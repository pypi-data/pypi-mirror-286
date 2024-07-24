#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

import copy
import itertools
import logging
from collections import defaultdict
from dataclasses import dataclass, field

from itertools import chain
from threading import Event, Thread
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from torch import distributed as dist
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.fx.node import Node
from torch.profiler import record_function
from torchrec.distributed.dist_data import KJTAllToAll, KJTAllToAllTensorsAwaitable
from torchrec.distributed.embedding_sharding import (
    FusedKJTListSplitsAwaitable,
    KJTListSplitsAwaitable,
    KJTSplitsAllToAllMeta,
)
from torchrec.distributed.model_parallel import DistributedModelParallel, ShardedModule

from torchrec.distributed.types import Awaitable

from torchrec.sparse.jagged_tensor import KeyedJaggedTensor
from torchrec.streamable import Multistreamable, Pipelineable


logger: logging.Logger = logging.getLogger(__name__)

import torch

In = TypeVar("In", bound=Pipelineable)
StageOut = TypeVar("StageOut", bound=Pipelineable)
Out = TypeVar("Out")

RunnableType = Callable[..., StageOut]
StageOutputWithEvent = Tuple[Optional[StageOut], Optional[torch.cuda.Event]]


@dataclass
class TrainPipelineContext:
    """
    Context information for a `TrainPipelineSparseDist` instance.

    Attributes:
        input_dist_splits_requests (Dict[str, Awaitable[Any]]): Stores input dist
            requests in the splits awaitable stage, which occurs after starting the
            input dist.
        input_dist_tensors_requests (Dict[str, Awaitable[Any]]): Stores input dist
            requests in the tensors awaitable stage, which occurs after calling `wait()`
            on the splits awaitable.
        module_contexts (Dict[str, Multistreamable]): Stores module contexts from the
            input dist for the current batch.
        module_contexts_next_batch (Dict[str, Multistreamable]): Stores module contexts
            from the input dist for the next batch. (only for version 0)
        fused_splits_awaitables (List[Tuple[List[str], FusedKJTListSplitsAwaitable]]):
            List of fused splits input dist awaitable and the corresponding module names
            of each awaitable.
        event: Optional[torch.cuda.Event]: Event to record the completion of this stage
        index: Optional[int]: Index of the current batch.
        version: int = 0; support for backward compatiblity
    """

    # pyre-ignore [4]
    input_dist_splits_requests: Dict[str, Awaitable[Any]] = field(default_factory=dict)
    # pyre-ignore [4]
    input_dist_tensors_requests: Dict[str, Awaitable[Any]] = field(default_factory=dict)
    module_contexts: Dict[str, Multistreamable] = field(default_factory=dict)
    module_contexts_next_batch: Dict[str, Multistreamable] = field(
        default_factory=dict
    )  # deprecated: to support legacy code
    fused_splits_awaitables: List[Tuple[List[str], FusedKJTListSplitsAwaitable]] = (
        field(default_factory=list)
    )
    event: Optional[torch.cuda.Event] = None
    index: Optional[int] = None
    version: int = (
        0  # 1 is current version, 0 is deprecated but supported for backward compatibility
    )


@dataclass
class PrefetchTrainPipelineContext(TrainPipelineContext):
    module_input_post_prefetch: Dict[str, Multistreamable] = field(default_factory=dict)
    module_contexts_post_prefetch: Dict[str, Multistreamable] = field(
        default_factory=dict
    )


@dataclass
class EmbeddingTrainPipelineContext(TrainPipelineContext):
    embedding_a2a_requests: Dict[str, Multistreamable] = field(default_factory=dict)


@dataclass
class PipelineStage:
    """
    A pipeline stage represents a transform to an input that is independent of the
    backwards() of the model. Examples include batch H2D transfer, GPU preproc, or
    gradient-less model processing.

    Args:
        name (str): Name of the stage.
        runnable (Callable[In, Out]): Function that performs a gradient-less
            transform.
        stream (torch.cuda.streams.Stream): Stream to run on. Often each stage has a
            unique stream, but having different pipelines share a stream provides more
            synchronization semantics.
    """

    name: str
    runnable: RunnableType
    stream: torch.cuda.streams.Stream
    fill_callback: Optional[Callable[[], None]] = None


@dataclass
class ArgInfo:
    """
    Representation of args from a node.

    Attributes:
        input_attrs (List[str]): attributes of input batch,
            e.g. `batch.attr1.attr2` will produce ["attr1", "attr2"].
        is_getitems (List[bool]): `batch[attr1].attr2` will produce [True, False].
        name (Optional[str]): name for kwarg of pipelined forward() call or None for a
            positional arg.
    """

    input_attrs: List[str]
    is_getitems: List[bool]
    name: Optional[str]


class BaseForward:
    def __init__(
        self,
        name: str,
        args: List[ArgInfo],
        module: ShardedModule,
        context: TrainPipelineContext,
        stream: Optional[torch.cuda.streams.Stream],
    ) -> None:
        self._name = name
        self._args = args
        self._module = module
        self._context = context
        self._stream = stream

    @property
    def name(self) -> str:
        return self._name

    @property
    def args(self) -> List[ArgInfo]:
        return self._args

    def set_context(self, context: TrainPipelineContext) -> None:
        self._context = context

    def get_context(self) -> TrainPipelineContext:
        return self._context


class PipelinedForward(BaseForward):
    # pyre-ignore [2, 24]
    def __call__(self, *input, **kwargs) -> Awaitable:
        assert (
            self._name in self._context.input_dist_tensors_requests
        ), "Invalid PipelinedForward usage, please do not directly call model.forward()"
        request = self._context.input_dist_tensors_requests.pop(self._name)
        assert isinstance(request, Awaitable)
        with record_function("## wait_sparse_data_dist ##"):
            # Finish waiting on the dist_stream,
            # in case some delayed stream scheduling happens during the wait() call.
            with torch.cuda.stream(self._stream):
                data = request.wait()

        # Make sure that both result of input_dist and context
        # are properly transferred to the current stream.
        ctx = self._context.module_contexts.pop(self._name)

        if self._stream is not None:
            torch.cuda.current_stream().wait_stream(self._stream)
            cur_stream = torch.cuda.current_stream()

            assert isinstance(
                data, (torch.Tensor, Multistreamable)
            ), f"{type(data)} must implement Multistreamable interface"
            data.record_stream(cur_stream)
            ctx.record_stream(cur_stream)

        return self._module.compute_and_output_dist(ctx, data)


class EmbeddingPipelinedForward(BaseForward):
    # pyre-ignore [2, 24]
    def __call__(self, *input, **kwargs) -> Awaitable:
        assert (
            self._name
            # pyre-ignore [16]
            in self._context.embedding_a2a_requests
        ), "Invalid EmbeddingPipelinedForward usage, please do not directly call model.forward()"

        ctx = self._context.module_contexts.pop(self._name)
        if self._stream is not None:
            torch.cuda.current_stream().wait_stream(self._stream)
            cur_stream = torch.cuda.current_stream()
            ctx.record_stream(cur_stream)
        return self._context.embedding_a2a_requests.pop(self._name)


class PrefetchPipelinedForward(BaseForward):
    def __init__(
        self,
        name: str,
        args: List[ArgInfo],
        module: ShardedModule,
        context: PrefetchTrainPipelineContext,
        prefetch_stream: Optional[torch.cuda.streams.Stream],
    ) -> None:
        super().__init__(
            name=name,
            args=args,
            module=module,
            context=context,
            stream=prefetch_stream,
        )

    # pyre-ignore [2, 24]
    def __call__(self, *input, **kwargs) -> Awaitable:

        assert (
            self._name
            # pyre-ignore [16]
            in self._context.module_input_post_prefetch
        ), "Invalid PrefetchPipelinedForward usage, please do not directly call model.forward()"
        data = self._context.module_input_post_prefetch.pop(self._name)
        # pyre-ignore [16]
        ctx = self._context.module_contexts_post_prefetch.pop(self._name)

        # Make sure that both result of input_dist and context
        # are properly transferred to the current stream.
        if self._stream is not None:
            torch.cuda.current_stream().wait_stream(self._stream)
            cur_stream = torch.cuda.current_stream()

            assert isinstance(
                data, (torch.Tensor, Multistreamable)
            ), f"{type(data)} must implement Multistreamable interface"
            data.record_stream(cur_stream)

            ctx.record_stream(cur_stream)

        return self._module.compute_and_output_dist(ctx, data)


class KJTAllToAllForward:
    def __init__(
        self, pg: dist.ProcessGroup, splits: List[int], stagger: int = 1
    ) -> None:
        self._pg = pg
        self._splits = splits
        self._stagger = stagger
        self._splits_cumsum: List[int] = [0] + list(itertools.accumulate(splits))

    def __call__(self, input: KeyedJaggedTensor) -> KJTSplitsAllToAllMeta:
        with torch.no_grad():
            assert len(input.keys()) == sum(self._splits)
            rank = dist.get_rank(self._pg)
            local_keys = input.keys()[
                self._splits_cumsum[rank] : self._splits_cumsum[rank + 1]
            ]
            input_splits = input.dist_splits(self._splits)
            device = input.values().device
            splits_tensors = [
                torch.tensor(splits, device=device) for splits in input_splits
            ]
            if not input.variable_stride_per_key():
                splits_tensors.append(
                    torch.tensor([input.stride()] * self._pg.size(), device=device)
                )
            return KJTSplitsAllToAllMeta(
                pg=self._pg,
                _input=input,
                splits=self._splits,
                splits_tensors=splits_tensors,
                input_splits=input_splits,
                input_tensors=input.dist_tensors(),
                labels=input.dist_labels(),
                keys=local_keys,
                device=device,
                stagger=self._stagger,
            )


class Tracer(torch.fx.Tracer):
    """
    Disables proxying buffers during tracing. Ideally, proxying buffers would be
    disabled, but some models are currently mutating buffer values, which causes errors
    during tracing. If those models can be rewritten to not do that, we can likely
    remove this line.
    """

    proxy_buffer_attributes = False

    def __init__(self, leaf_modules: Optional[List[str]] = None) -> None:
        super().__init__()
        self._leaf_modules: List[str] = leaf_modules if leaf_modules is not None else []

    def is_leaf_module(self, m: torch.nn.Module, module_qualified_name: str) -> bool:
        if (
            isinstance(m, ShardedModule)
            or module_qualified_name in self._leaf_modules
            or isinstance(m, FSDP)
        ):
            return True
        return super().is_leaf_module(m, module_qualified_name)


def _to_device(batch: In, device: torch.device, non_blocking: bool) -> In:
    assert isinstance(
        batch, (torch.Tensor, Pipelineable)
    ), f"{type(batch)} must implement Pipelineable interface"
    return cast(In, batch.to(device=device, non_blocking=non_blocking))


def _wait_for_batch(batch: In, stream: Optional[torch.cuda.streams.Stream]) -> None:
    """
    As mentioned in
    https://pytorch.org/docs/stable/generated/torch.Tensor.record_stream.html, PyTorch
    uses the "caching allocator" for memory allocation for tensors. When a tensor is
    freed, its memory is likely to be reused by newly constructed tenosrs. By default,
    this allocator traces whether a tensor is still in use by only the CUDA stream where
    it was created. When a tensor is used by additional CUDA streams, we need to call
    `record_stream` to tell the allocator about these streams. Otherwise, the allocator
    might free the underlying memory of the tensor once it is no longer used by the
    creator stream. This is a notable programming trick when we write programs using
    multiple CUDA streams.
    """
    if stream is None:
        return
    torch.cuda.current_stream().wait_stream(stream)

    cur_stream = torch.cuda.current_stream()
    assert isinstance(
        batch, (torch.Tensor, Multistreamable)
    ), f"{type(batch)} must implement Multistreamable interface"
    batch.record_stream(cur_stream)


def _wait_for_event(batch: In, event: Optional[torch.cuda.Event]) -> None:
    """
    Wait for event
    """
    if event is not None:
        event.wait()
    cur_stream = torch.cuda.current_stream()

    assert isinstance(
        batch, (torch.Tensor, Multistreamable)
    ), f"{type(batch)} must implement Multistreamable interface"
    batch.record_stream(cur_stream)


def _start_data_dist(
    pipelined_modules: List[ShardedModule],
    batch: In,
    context: TrainPipelineContext,
) -> None:
    if context.version == 0:
        context.input_dist_splits_requests.clear()
        context.module_contexts_next_batch.clear()
        context.fused_splits_awaitables.clear()

    for module in pipelined_modules:
        forward = module.forward
        assert (
            isinstance(forward, PipelinedForward)
            or isinstance(forward, PrefetchPipelinedForward)
            or isinstance(forward, EmbeddingPipelinedForward)
        )

        # Retrieve argument for the input_dist of EBC
        # is_getitem True means this argument could be retrieved by a list
        # False means this argument is getting while getattr
        # and this info was done in the _rewrite_model by tracing the
        # entire model to get the arg_info_list
        args = []
        kwargs = {}
        for arg_info in forward.args:
            if arg_info.input_attrs:
                arg = batch
                for attr, is_getitem in zip(arg_info.input_attrs, arg_info.is_getitems):
                    if is_getitem:
                        arg = arg[attr]
                    else:
                        arg = getattr(arg, attr)
                if arg_info.name:
                    kwargs[arg_info.name] = arg
                else:
                    args.append(arg)
            else:
                args.append(None)
        # Start input distribution.
        module_ctx = module.create_context()
        if context.version == 0:
            context.module_contexts_next_batch[forward.name] = module_ctx
        else:
            context.module_contexts[forward.name] = module_ctx
        context.input_dist_splits_requests[forward.name] = module.input_dist(
            module_ctx, *args, **kwargs
        )
    _fuse_input_dist_splits(context)


def _start_embedding_lookup(
    pipelined_modules: List[ShardedModule],
    batch: In,  # not used in this function
    context: EmbeddingTrainPipelineContext,
) -> None:
    cur_stream = torch.cuda.current_stream()
    kjts_per_module = []
    for module in pipelined_modules:
        kjts = context.input_dist_tensors_requests[module.forward.name].wait()
        kjts.record_stream(cur_stream)
        kjts_per_module.append(kjts)

    for module, kjts in zip(pipelined_modules, kjts_per_module):
        module_name = module.forward.name
        module_context = context.module_contexts[module.forward.name]
        module_context.record_stream(cur_stream)
        a2a_awaitable = module.compute_and_output_dist(module_context, kjts)
        # pyre-ignore[6]
        context.embedding_a2a_requests[module_name] = a2a_awaitable


def _fuse_input_dist_splits(context: TrainPipelineContext) -> None:
    names_per_pg = defaultdict(list)
    for name, request in context.input_dist_splits_requests.items():
        pg = None
        if isinstance(request, KJTListSplitsAwaitable):
            for awaitable in request.awaitables:
                if isinstance(awaitable, KJTSplitsAllToAllMeta):
                    pg = awaitable.pg
                    break
        names_per_pg[pg].append(name)

    for pg, names in names_per_pg.items():
        context.fused_splits_awaitables.append(
            (
                names,
                FusedKJTListSplitsAwaitable(
                    # pyre-ignore[6]
                    requests=[
                        context.input_dist_splits_requests[name] for name in names
                    ],
                    contexts=[
                        (
                            context.module_contexts_next_batch[name]
                            if context.version == 0
                            else context.module_contexts[name]
                        )
                        for name in names
                    ],
                    pg=pg,
                ),
            )
        )


def _check_args_for_call_module(
    node: torch.fx.Node,
) -> bool:
    """
    Recursively checks if args to a node is the result of a call_module.
    """
    if node.op == "call_module":
        return True

    for arg in node.args:
        if isinstance(arg, torch.fx.Node) and _check_args_for_call_module(arg):
            return True

    return False


def _get_node_args_helper(
    # pyre-ignore
    arguments,
    num_found: int,
) -> Tuple[List[ArgInfo], int]:
    """
    Goes through the args/kwargs of a node and arranges them into a list of `ArgInfo`s.
    It also counts the number of (args + kwargs) found.
    """

    arg_info_list = [ArgInfo([], [], None) for _ in range(len(arguments))]
    for arg, arg_info in zip(arguments, arg_info_list):
        if arg is None:
            num_found += 1
            continue
        while True:
            if not isinstance(arg, torch.fx.Node):
                break
            child_node = arg

            if child_node.op == "placeholder":
                if hasattr(child_node, "ph_key"):
                    # pyre-ignore[16]
                    arg_info.input_attrs.insert(0, child_node.ph_key)
                    arg_info.is_getitems.insert(0, False)
                num_found += 1
                break
            elif (
                child_node.op == "call_function"
                and child_node.target.__module__ == "builtins"
                # pyre-ignore[16]
                and child_node.target.__name__ == "getattr"
            ):
                # pyre-fixme[6]: For 2nd argument expected `str` but got
                #  `Union[None, Dict[str, typing.Any], List[typing.Any], Node, bool,
                #  complex, float, int, range, slice, str, device, dtype, layout,
                #  memory_format, Tensor, typing.Tuple[typing.Any, ...]]`.
                arg_info.input_attrs.insert(0, child_node.args[1])
                arg_info.is_getitems.insert(0, False)
                arg = child_node.args[0]
            elif (
                child_node.op == "call_function"
                and child_node.target.__module__ == "_operator"
                # pyre-ignore[16]
                and child_node.target.__name__ == "getitem"
            ):
                # pyre-fixme[6]: For 2nd argument expected `str` but got
                #  `Union[None, Dict[str, typing.Any], List[typing.Any], Node, bool,
                #  complex, float, int, range, slice, str, device, dtype, layout,
                #  memory_format, Tensor, typing.Tuple[typing.Any, ...]]`.
                arg_info.input_attrs.insert(0, child_node.args[1])
                arg_info.is_getitems.insert(0, True)
                arg = child_node.args[0]
            elif (
                child_node.op == "call_function"
                and child_node.target.__module__ == "torch.utils._pytree"
                # pyre-ignore[16]
                and child_node.target.__name__ == "tree_unflatten"
            ):
                """
                This is for the PT2 export path where we unflatten the input to reconstruct
                the structure with the recorded tree spec.
                """
                assert arg_info.is_getitems[0]
                # pyre-fixme[16]
                arg = child_node.args[0][arg_info.input_attrs[0]]
            elif (
                child_node.op == "call_function"
                and child_node.target.__module__ == "torchrec.sparse.jagged_tensor"
                # pyre-fixme[16]
                and child_node.target.__name__ == "KeyedJaggedTensor"
            ):
                call_module_found = False

                for arg_node in chain(child_node.args, child_node.kwargs.values()):
                    if isinstance(
                        arg_node, torch.fx.Node
                    ) and _check_args_for_call_module(arg_node):
                        call_module_found = True
                        break

                if call_module_found:
                    break

                if "values" in child_node.kwargs:
                    arg = child_node.kwargs["values"]
                else:
                    arg = child_node.args[1]
            else:
                break
    return arg_info_list, num_found


def _get_node_args(
    node: Node,
) -> Tuple[List[ArgInfo], int]:
    num_found = 0
    pos_arg_info_list, num_found = _get_node_args_helper(node.args, num_found)
    kwargs_arg_info_list, num_found = _get_node_args_helper(
        node.kwargs.values(), num_found
    )

    # Replace with proper names for kwargs
    for name, arg_info_list in zip(node.kwargs, kwargs_arg_info_list):
        arg_info_list.name = name

    arg_info_list = pos_arg_info_list + kwargs_arg_info_list
    return arg_info_list, num_found


def _get_leaf_module_names_helper(
    model: torch.nn.Module,
    path: str,
    leaf_module_names: Set[str],
) -> bool:
    sharded_children = set()
    for name, child in model.named_children():
        curr_path = path + name
        if isinstance(child, ShardedModule):
            sharded_children.add(name)
        else:
            child_sharded = _get_leaf_module_names_helper(
                child,
                curr_path + ".",
                leaf_module_names,
            )
            if child_sharded:
                sharded_children.add(name)

    if len(sharded_children) > 0:
        for name, child in model.named_children():
            if name in sharded_children:
                continue
            # assume module is leaf node unless annotated otherwise
            if not getattr(child, "_is_pytorch_fx_traceable", False):
                leaf_module_names.add(path + name)
    return len(sharded_children) > 0


def _get_leaf_module_names(model: torch.nn.Module) -> List[str]:
    """
    Returns a list of top level modules to be used as leaf modules for FX tracing.
    This is a shallow FX trace that only goes the minimum depth required to pipeline
    the model unless child modules are explicitly tagged as `_is_pytorch_fx_traceable`.
    """

    leaf_module_names: Set[str] = set()
    _get_leaf_module_names_helper(
        model,
        "",
        leaf_module_names,
    )
    return list(leaf_module_names)


def _jit_modules(module: torch.nn.Module, path: str, optional: bool = True) -> bool:
    sharded_children = set()
    for name, child in module.named_children():
        curr_path = path + name
        if isinstance(child, ShardedModule):
            sharded_children.add(name)
        else:
            child_sharded = _jit_modules(child, curr_path + ".", optional)
            if child_sharded:
                sharded_children.add(name)

    if len(sharded_children) > 0:
        for name, child in module.named_children():
            if name not in sharded_children:
                try:
                    jit_child = torch.jit.script(child)
                    setattr(module, name, jit_child)
                    logger.info(f"jit.script applied to {path + name}.")
                except Exception as error:
                    if not optional:
                        raise
                    else:
                        logger.info(
                            f"Warning: failed to jit.script {path + name}: {error}."
                        )

    return len(sharded_children) > 0


def _pipeline_detach_model(
    pipelined_modules: List[ShardedModule],
    # pyre-ignore[2]
    original_forwards: List[Callable[..., Any]],
    original_kjt_dist_forwards: List[
        Callable[[KeyedJaggedTensor], Awaitable[KJTAllToAllTensorsAwaitable]]
    ],
) -> None:
    kjt_dists = []
    for mod, original_fwd in zip(pipelined_modules, original_forwards):
        # pyre-ignore
        mod.forward = original_fwd

        for _, child_module in mod.named_modules():
            if not hasattr(child_module, "_input_dists"):
                continue
            for input_dist in child_module._input_dists:
                if hasattr(input_dist, "_dist"):
                    kjt_dists.append(input_dist._dist)
    assert len(kjt_dists) == len(
        original_kjt_dist_forwards
    ), f"Number of KJT dists ({len(kjt_dists)}) does not match number of kjt dist forwards provided ({len(original_kjt_dist_forwards)})"

    for kjt_dist, original_kjt_dist_fwd in zip(
        kjt_dists,
        original_kjt_dist_forwards,
    ):
        kjt_dist.forward = original_kjt_dist_fwd


# pyre-ignore[3]
def _rewrite_model(  # noqa C901
    model: torch.nn.Module,
    context: TrainPipelineContext,
    dist_stream: Optional[torch.cuda.streams.Stream],
    batch: Optional[In] = None,
    apply_jit: bool = False,
    pipelined_forward: Type[BaseForward] = PipelinedForward,
) -> Tuple[List[ShardedModule], torch.nn.Module, List[Callable[..., Any]]]:
    input_model = model
    # Get underlying nn.Module
    if isinstance(model, DistributedModelParallel):
        model = model.module

    # Collect a list of sharded modules.
    sharded_modules = {}
    for name, m in model.named_modules():
        if isinstance(m, ShardedModule):
            sharded_modules[name] = m

    # Trace a model.
    concrete_args = {}
    if batch:
        if hasattr(batch, "to_proxy"):
            # for some special models, it requires using "input"
            # as the key for input
            # pyre-ignore[16]: Variable[In (bound to Pipelineable)] has no attribute to_proxy.
            concrete_args["inputs"] = copy.copy(batch).to_proxy()
        elif hasattr(batch, "to_proxy_tuple"):
            # when the model is pre-fx traced or dynamo exported, the
            # inputs are already flattened, and therefore we use
            # tuple as concrete args that fx.trace will automatically
            # match with the argument names.
            # We pass in the model for the caller side to customize
            # the batch
            # pyre-ignore[16]: Variable[In (bound to Pipelineable)] has no attribute to_proxy_tuple.
            concrete_args = batch.to_proxy_tuple(model)

    tracer = Tracer(leaf_modules=_get_leaf_module_names(model))
    graph = tracer.trace(model, concrete_args=concrete_args)

    # Select sharded modules, which are top-level in the forward call graph,
    # i.e. don't have input transformations, i.e. rely only on 'builtins.getattr'.
    pipelined_forwards = []
    original_forwards = []
    for node in graph.nodes:
        if node.op == "call_module" and node.target in sharded_modules:
            total_num_args = len(node.args) + len(node.kwargs)
            if total_num_args == 0:
                continue
            arg_info_list, num_found = _get_node_args(node)

            if num_found == total_num_args:
                logger.info(f"Module '{node.target}'' will be pipelined")
                child = sharded_modules[node.target]
                original_forwards.append(child.forward)
                child.forward = pipelined_forward(
                    node.target,
                    arg_info_list,
                    child,
                    context,
                    dist_stream,
                )
                pipelined_forwards.append(child)
            else:
                logger.warning(
                    f"Module '{node.target}'' will not be pipelined, due to input modifications"
                )

    # JIT script unsharded modules if applicable.
    if apply_jit:
        graph_model = torch.fx.GraphModule(model, graph)
        _jit_modules(graph_model, "")
        if isinstance(input_model, DistributedModelParallel):
            input_model.module = graph_model

    return pipelined_forwards, input_model, original_forwards


def _override_input_dist_forwards(
    pipelined_modules: List[ShardedModule],
) -> List[Callable[[KeyedJaggedTensor], Awaitable[KJTAllToAllTensorsAwaitable]]]:
    """
    Overrides each input dist forward to support fusing the splits collective.
    NOTE: this can only be called after the input dists are initialized.
    """
    original_kjt_dist_forwards = []
    for module in pipelined_modules:
        for child_fqn, child_module in module.named_modules():
            if hasattr(child_module, "_has_uninitialized_input_dist"):
                assert (
                    not child_module._has_uninitialized_input_dist
                ), f"{child_fqn} has uninitialized input dist"

            if not hasattr(child_module, "_input_dists"):
                continue

            for input_dist in child_module._input_dists:
                if hasattr(input_dist, "_dist"):
                    assert isinstance(input_dist._dist, KJTAllToAll)
                    original_kjt_dist_forwards.append(input_dist._dist.forward)
                    input_dist._dist.forward = KJTAllToAllForward(
                        pg=input_dist._dist._pg,
                        splits=input_dist._dist._splits,
                        stagger=input_dist._dist._stagger,
                    )
    return original_kjt_dist_forwards


def get_h2d_func(batch: In, device: torch.device) -> Pipelineable:
    return batch.to(device, non_blocking=True)


class DataLoadingThread(Thread, Generic[In]):
    def __init__(
        self,
        device: torch.device,
        dataloader_iter: Iterator[In],
        to_device_non_blocking: bool,
        memcpy_stream_priority: int = 0,
    ) -> None:
        super().__init__()
        self._stop: bool = False
        self._dataloader_iter = dataloader_iter
        self._buffer_empty_event: Event = Event()
        self._buffer_filled_event: Event = Event()
        self._memcpy_stream: Optional[torch.cuda.streams.Stream] = (
            torch.cuda.Stream(priority=memcpy_stream_priority)
            if device.type == "cuda"
            else None
        )
        self._device = device
        self._to_device_non_blocking = to_device_non_blocking
        self._buffered: Optional[In] = None
        self._buffer_empty_event.set()

    def run(self) -> None:
        if self._device.type == "cuda" and torch.cuda.is_available():
            # set the current device the same as the one used in the main thread
            torch.cuda.set_device(self._device)

        while not self._stop:
            self._buffer_empty_event.wait()
            # Set the filled event to unblock progress() and return.
            if self._stop:
                self._buffer_filled_event.set()
                return
            with record_function("## load_batch ##"):
                try:
                    batch = next(self._dataloader_iter)
                except StopIteration:
                    self._stop = True
                    self._buffer_filled_event.set()
                    return
            with record_function("## copy_batch_to_gpu ##"):
                with torch.cuda.stream(self._memcpy_stream):
                    self._buffered = cast(
                        In,
                        batch.to(
                            self._device, non_blocking=self._to_device_non_blocking
                        ),
                    )
                self._buffer_empty_event.clear()
                self._buffer_filled_event.set()

    def stop(self) -> None:
        logger.info("Stopping data loading thread...")
        self._stop = True
        # Unblock any thread that are waiting for these events.
        self._buffer_filled_event.set()
        self._buffer_empty_event.set()
        logger.info("Data loading thread stopped.")

    def get_next_batch(self, none_throws: bool = False) -> Optional[In]:
        """
        Get the next batch from the buffer if threading is enabled, otherwise
        call load_next_batch directly.

        This function is not thread safe. We assume this is only invoked from
        the main thread in the training loop.
        """
        self._buffer_filled_event.wait()
        batch = self._buffered
        if batch is None:
            if none_throws:
                raise StopIteration
            return None
        self._buffered = None
        self._buffer_filled_event.clear()
        self._buffer_empty_event.set()
        return batch


class SparseDataDistUtil(Generic[In]):
    def __init__(
        self,
        model: torch.nn.Module,
        stream: torch.cuda.streams.Stream,
        apply_jit: bool = False,
    ) -> None:
        super().__init__()
        self.model = model
        self.stream = stream
        self.apply_jit = apply_jit
        self.context = TrainPipelineContext(version=0)
        self.initialized = False
        self._pipelined_modules: List[ShardedModule] = []
        # pyre-ignore
        self.fwd_hook = None

        # pyre-ignore
        self._original_forwards: List[Callable[..., Any]] = []
        self._original_kjt_dist_forwards: List[
            Callable[[KeyedJaggedTensor], Awaitable[KJTAllToAllTensorsAwaitable]]
        ] = []

    def detach(self) -> torch.nn.Module:
        """
        Removes sparse data dist (SDD) pipelining from model forward and input dist.
        Modifies existing model in place and returns the model.

        detach() can be called at any point, and inflight batches do not need to be
        flushed before calling it. Calling pipeline.progress() will re-attach the model
        to the pipeline and the pipeline will progress normally from the point it was detached (i.e. inflight batches will be kept when calling detach).

        While the model is detached, it is equivalent to the model before passing to
        the pipeline, so forward and backward passes, and optimizer updates can be
        carried out normally.
        """
        if self.initialized:
            assert self.fwd_hook is not None
            self.fwd_hook.remove()

            _pipeline_detach_model(
                pipelined_modules=self._pipelined_modules,
                original_forwards=self._original_forwards,
                original_kjt_dist_forwards=self._original_kjt_dist_forwards,
            )

        self.initialized = False
        return self.model

    def start_sparse_data_dist(self, batch: In) -> In:
        if not self.initialized:
            # Step 1: Pipeline input dist in trec sharded modules
            self._pipelined_modules, self.model, self._original_forwards = (
                _rewrite_model(
                    model=self.model,
                    context=self.context,
                    dist_stream=self.stream,
                    batch=batch,
                    apply_jit=self.apply_jit,
                )
            )
            # initializes input dist, so we can override input dist forwards
            _start_data_dist(self._pipelined_modules, batch, self.context)
            self._original_kjt_dist_forwards = _override_input_dist_forwards(
                self._pipelined_modules
            )

            # Step 2: Register post-forward hook to wait SDD
            def forward_hook(
                module: torch.nn.Module,
                input: Union[torch.Tensor, Tuple[torch.Tensor]],
                output: Union[torch.Tensor, Tuple[torch.Tensor]],
            ) -> None:
                self.wait_sparse_data_dist()

            self.fwd_hook = self.model.register_forward_hook(forward_hook)

            self.initialized = True

        _start_data_dist(self._pipelined_modules, batch, self.context)

        return batch

    def wait_sparse_data_dist(self) -> None:
        with record_function("## wait_sparse_data_dist ##"):
            with torch.cuda.stream(self.stream):
                self.context.module_contexts = (
                    self.context.module_contexts_next_batch.copy()
                )
                self.context.input_dist_tensors_requests.clear()
                for names, awaitable in self.context.fused_splits_awaitables:
                    for name, request in zip(names, awaitable.wait()):
                        self.context.input_dist_tensors_requests[name] = request
