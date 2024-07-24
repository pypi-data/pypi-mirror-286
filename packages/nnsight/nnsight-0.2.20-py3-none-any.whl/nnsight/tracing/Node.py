from __future__ import annotations

import inspect
import weakref
from typing import (TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple,
                    Union)

import torch
from torch._subclasses.fake_tensor import FakeTensor

from .. import util
from ..logger import logger
from .Proxy import Proxy

if TYPE_CHECKING:
    from .Graph import Graph


class Node:
    """A Node represents some action that should be carried out during execution of a Graph.

    Attributes:
        name (str): Unique name of node.
        graph (Graph): Reference to parent Graph object.
        proxy_value (Any): Meta version of value. Used when graph has validate = True.
        target (Union[Callable, str]): Function to execute or reserved string name.
        args (List[Any], optional): Positional arguments. Defaults to None.
        kwargs (Dict[str, Any], optional): Keyword arguments. Defaults to None.
        listeners (List[Node]): Nodes that depend on this node.
        dependencies (List[Node]): Nodes that this node depends on.
        value (Any): Actual value to be populated during execution.
    """

    def __init__(
        self,
        name: str,
        graph: "Graph",
        value: Any,
        target: Union[Callable, str],
        args: List[Any] = None,
        kwargs: Dict[str, Any] = None,
    ) -> None:
        super().__init__()

        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()

        self.name = name
        self.graph: "Graph" = graph
        self.proxy_value = value
        self.target = target
        self.args: List = util.apply(args, lambda x: x.node, Proxy)
        self.kwargs: Dict = util.apply(kwargs, lambda x: x.node, Proxy)

        self.proxy: Optional[Proxy] = None

        self.value: Any = inspect._empty

        self.listeners: List[Node] = list()
        self.dependencies: List[Node] = list()

        # Resolve values from completed tracer/runner contexts
        self.args = util.apply(self.args, lambda x: x.value if x.done() else x, Node)
        self.kwargs = util.apply(
            self.kwargs, lambda x: x.value if x.done() else x, Node
        )

        # Add all arguments that are nodes to nodes dependencies
        # (unless the arg is already .done(), for when you want to apply things to proxies after model execution?)
        util.apply(
            self.args,
            lambda x: self.dependencies.append(x) if not x.done() else None,
            Node,
        )
        util.apply(
            self.kwargs,
            lambda x: self.dependencies.append(x) if not x.done() else None,
            Node,
        )
        # Add node to all arguments that are nodes' listeners
        # (unless the arg is already .done(), for when you want to apply things to proxies after model execution?)
        util.apply(
            self.args,
            lambda x: x.listeners.append(weakref.proxy(self)) if not x.done() else None,
            Node,
        )
        util.apply(
            self.kwargs,
            lambda x: x.listeners.append(weakref.proxy(self)) if not x.done() else None,
            Node,
        )

        self.remaining_listeners = 0
        self.remaining_dependencies = 0

        self.compile()

        # (for when you want to apply things to proxies after model execution)
        if self.fulfilled() and not isinstance(self.target, str):
            # So it doesn't get destroyed.
            self.remaining_listeners = 1

            self.execute()

    def is_tracing(self) -> bool:
        """Checks to see if the weakref to the Graph is alive and tracing or dead.

        Returns:
            bool: Is Graph tracing.
        """

        try:

            return self.graph.tracing

        except:
            return False

    def add(
        self,
        target: Union[Callable, str],
        value: Any = inspect._empty,
        args: List[Any] = None,
        kwargs: Dict[str, Any] = None,
        name: str = None,
    ) -> Proxy:
        """We use Node.add vs Graph.add in case the weakref to Graph is gone.

        Returns:
            Proxy: Proxy
        """

        if not self.is_tracing():

            return Proxy(
                Node(
                    name=None,
                    graph=None,
                    value=None,
                    target=target,
                    args=args,
                    kwargs=kwargs,
                )
            ).value

        return self.graph.add(
            target=target, value=value, args=args, kwargs=kwargs, name=name
        )

    def compile(self) -> None:
        """Resets this Nodes remaining_listeners and remaining_dependencies and sets its value to None."""
        self.remaining_listeners = len(self.listeners)
        self.remaining_dependencies = len(self.dependencies)
        self.value = inspect._empty

    def done(self) -> bool:
        """Returns true if the value of this node has been set.

        Returns:
            bool: If done.
        """
        return self.value is not inspect._empty

    def fulfilled(self) -> bool:
        """Returns true if remaining_dependencies is 0.

        Returns:
            bool: If fulfilled.
        """
        return self.remaining_dependencies == 0

    def redundant(self) -> bool:
        """Returns true if remaining_listeners is 0.

        Returns:
            bool: If redundant.
        """
        return self.remaining_listeners == 0

    @classmethod
    def prepare_inputs(
        cls, inputs: Any, device: torch.device = None, proxy: bool = False
    ) -> Any:
        """Prepare arguments for executing this node's target.
        Converts Nodes in args and kwargs to their value and moves tensors to correct device.
        Returns:
            Any: Prepared inputs.
        """

        inputs = util.apply(inputs, lambda x: x, inspect._empty)

        def _value(node: Proxy | Node):

            if isinstance(node, Proxy):
                node = node.node

            if proxy:
                return node.proxy_value

            return node.value

        inputs = util.apply(inputs, _value, (Node, Proxy), inplace=not proxy)

        if device is None:

            def _device(value: torch.Tensor):

                nonlocal device

                if device is None:
                    device = value.device

            util.apply(inputs, _device, torch.Tensor)

        def _to(value: torch.Tensor):
            return value.to(device)

        inputs = util.apply(inputs, _to, torch.Tensor, inplace=not proxy)

        return inputs

    def execute(self) -> None:
        """Actually executes this node.
        If target is 'null' do nothing.
        Prepares args and kwargs and passed them to target.
        """

        # Prepare arguments.
        args, kwargs = Node.prepare_inputs((self.args, self.kwargs))

        # We se a nodes target to 'null' if we don't want it to be executed and therefore never done
        if self.target == "null":
            return
        elif self.target == "swap":
            if self.graph.swap is not None:
                self.graph.swap.set_value(False)

            self.graph.swap = self

            return

        elif self.target == "grad":

            tensor: torch.Tensor = args[0]
            backward_idx: int = args[1]

            hook = None

            def grad(value):

                nonlocal backward_idx
                nonlocal hook

                if backward_idx == 0:

                    self.set_value(value)

                    if self.is_tracing():

                        value = self.graph.get_swap(value)

                    backward_idx = -1

                    hook.remove()

                    return value

                else:

                    backward_idx -= 1

                    return None

            hook = tensor.register_hook(lambda value: grad(value))

            return

        # Call the target to get value.
        output = self.target(*args, **kwargs)

        self.set_value(output)

    def set_value(self, value: Any):
        """Sets the value of this Node and logs the event.
        Updates remaining_dependencies of listeners. If they are now fulfilled, execute them.
        Updates remaining_listeners of dependencies. If they are now redundant, destroy them.

        Args:
            value (Any): Value.
        """
        self.value = value

        logger.info(f"=> SET({self.name})")

        for listener in self.listeners:
            listener.remaining_dependencies -= 1

            if listener.fulfilled():
                listener.execute()

        for dependency in self.dependencies:
            dependency.remaining_listeners -= 1

            if dependency.redundant():
                dependency.destroy()

        if self.done() and self.redundant():
            self.destroy()

    def destroy(self) -> None:
        """Removes the reference to the node's value and logs it's destruction."""
        logger.info(f"=> DEL({self.name})")

        self.value = inspect._empty

    def __str__(self) -> str:
        args = util.apply(self.args, lambda x: f"'{x}'", str)
        args = util.apply(args, lambda x: x.name, Node)
        args = [str(arg) for arg in args]
        return f"{self.name}:[args:({','.join(args)}) l:{len(self.listeners)} d:{len(self.dependencies)}]"
