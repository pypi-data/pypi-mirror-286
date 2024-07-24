import inspect
import asyncio
import itertools
from typing import (
    TypeVar,
    ParamSpec,
    Callable,
    List,
    Tuple,
    Dict,
    Set,
    Iterable,
    Iterator,
    Sequence,
    MutableSequence,
    cast,
    Type,
    Awaitable,
    Any,
    Optional,
    Mapping,
    MutableMapping,
    get_type_hints,
    is_typeddict,
)
from functools import wraps, reduce

import networkx as nx
from typing_extensions import get_args, get_origin
from typing_inspect import is_union_type, get_generic_type
from typeguard import check_type, CollectionCheckStrategy
from mapgraph.typevar import (
    iter_deep_type,
    gen_typevar_model,
    extract_typevar_mapping,
    check_typevar_model,
)
from mapgraph.type_utils import (
    is_structural_type,
    deep_type,
    is_protocol_type,
    check_protocol_type,
    like_isinstance,
)

from ..type_utils import get_subclass_types, get_connected_subgraph


T = TypeVar("T")
In = TypeVar("In", contravariant=True)
Out = TypeVar("Out")
P = ParamSpec("P")


class TypeConverter:
    instances: List["TypeConverter"] = []

    def __init__(self):
        self.G = nx.DiGraph()
        self.sG = nx.DiGraph()
        self.pG = nx.DiGraph()
        self.tG = nx.DiGraph()
        self.pmG = nx.DiGraph()
        self.qG = nx.DiGraph()
        TypeConverter.instances.append(self)

    def get_graph(
        self,
        sub_class: bool = False,
        protocol: bool = False,
        combos: Optional[list[nx.DiGraph]] = None,
    ):
        base_graphs = [self.G]
        if sub_class:
            base_graphs.append(self.sG)
        if protocol:
            base_graphs.append(self.pG)

        if combos:
            base_graphs.extend(combos)

        if len(base_graphs) > 1:
            return nx.compose_all(base_graphs)
        return self.G

    def _gen_edge(
        self, in_type: Type[In], out_type: Type[Out], converter: Callable[P, Out]
    ):
        self.G.add_edge(in_type, out_type, converter=converter, line=True)
        for sub_in_type in self.get_subclass_types(in_type):
            self.sG.add_edge(
                sub_in_type,
                out_type,
                converter=converter,
                line=False,
                metadata={"sub_class": True},
            )
        if is_protocol_type(in_type):
            self.pmG.add_node(in_type)
        if is_protocol_type(out_type):
            self.pmG.add_node(out_type)
        for p_type in self.get_protocol_types(in_type):
            self.pG.add_edge(
                in_type,
                p_type,
                converter=lambda x: x,
                line=False,
                metadata={"protocol": True},
            )
        for p_type in self.get_protocol_types(out_type):
            self.pG.add_edge(
                out_type,
                p_type,
                converter=lambda x: x,
                line=False,
                metadata={"protocol": True},
            )

    def _gen_graph(self, in_type: Type[In], out_type: Type[Out]):
        tmp_G = nx.DiGraph()
        im = gen_typevar_model(in_type)
        om = gen_typevar_model(out_type)

        def _gen_sub_graph(mapping, node):
            for su, sv, sc in get_connected_subgraph(self.tG, node).edges(data=True):
                tmp_G.add_edge(su.get_instance(mapping), sv.get_instance(mapping), **sc)

        for u, v, c in self.tG.edges(data=True):
            um = gen_typevar_model(u)
            vm = gen_typevar_model(v)
            combos = [(um, im), (vm, im), (um, om), (vm, om)]
            for t, i in combos:
                try:
                    mapping = extract_typevar_mapping(t, i)
                    tmp_G.add_edge(
                        um.get_instance(mapping), vm.get_instance(mapping), **c
                    )
                    _gen_sub_graph(mapping, t)
                except Exception:
                    ...
        self.qG = nx.compose(self.qG, tmp_G)
        return tmp_G

    def register_generic_converter(self, input_type: Type, out_type: Type):
        def decorator(func: Callable[P, T]):
            self.tG.add_edge(input_type, out_type, converter=func)
            return func

        return decorator

    def register_converter(self, input_type: Type[In], out_type: Type[Out]):
        def decorator(func: Callable[P, T]) -> Callable[P, Out]:
            self._gen_edge(input_type, out_type, func)
            return cast(Callable[P, Out], func)

        return decorator

    def async_register_converter(self, input_type: Type[In], out_type: Type[Out]):
        def decorator(func: Callable[P, Awaitable[Out]]):
            self._gen_edge(input_type, out_type, func)
            return func

        return decorator

    def can_convert(
        self,
        in_type: Type[In],
        out_type: Type[Out],
        sub_class=False,
        protocol=False,
        combos: Optional[list[nx.DiGraph]] = None,
    ) -> bool:
        try:
            nx.has_path(
                self.get_graph(sub_class=sub_class, protocol=protocol, combos=combos),
                in_type,
                out_type,
            )
            res = True
        except nx.NodeNotFound:
            res = False
        return res

    def get_converter(
        self,
        in_type: Type[In],
        out_type: Type[Out],
        sub_class=False,
        protocol=False,
        input_value: Any = None,
    ):
        """
        [X] SubClass type
        [X] Union type
        [X] Annotated type
        [X] Structural type
        [ ] Generic type
        """

        for path, converters in self.get_all_paths(
            in_type, out_type, sub_class=sub_class, protocol=protocol
        ):
            func = reduce(lambda f, g: lambda x: g(f(x)), converters)
            yield path, func
        if is_union_type(out_type):
            for out_type in get_args(out_type):
                for path, converters in self.get_all_paths(
                    in_type, out_type, sub_class=sub_class, protocol=protocol
                ):
                    func = reduce(lambda f, g: lambda x: g(f(x)), converters)
                    yield path, func
                for p_type in self.get_check_types_by_value(
                    input_value, sub_class=sub_class, protocol=protocol
                ):
                    for path, converters in self.get_all_paths(
                        p_type, out_type, sub_class=sub_class, protocol=protocol
                    ):
                        func = reduce(lambda f, g: lambda x: g(f(x)), converters)
                        yield path, func
        for p_type in self.get_check_types_by_value(
            input_value, sub_class=sub_class, protocol=protocol
        ):
            for path, converters in self.get_all_paths(
                p_type, out_type, sub_class=sub_class, protocol=protocol
            ):
                func = reduce(lambda f, g: lambda x: g(f(x)), converters)
                yield path, func

    async def async_get_converter(
        self,
        in_type: Type[In],
        out_type: Type[Out],
        sub_class: bool = False,
        protocol: bool = False,
        input_value=None,
    ):
        def async_wrapper(converters):
            async def async_converter(input_value):
                for converter in converters:
                    if inspect.iscoroutinefunction(converter):
                        input_value = await converter(input_value)
                    else:
                        input_value = converter(input_value)
                return input_value

            return async_converter

        for path, converters in self.get_all_paths(
            in_type, out_type, sub_class=sub_class, protocol=protocol
        ):
            yield path, async_wrapper(converters)
        for p_type in self.get_check_types_by_value(
            input_value, sub_class=sub_class, protocol=protocol
        ):
            for path, converters in self.get_all_paths(
                p_type, out_type, sub_class=sub_class, protocol=protocol
            ):
                yield path, async_wrapper(converters)
        if is_union_type(out_type):
            for out_type in get_args(out_type):
                for path, converters in self.get_all_paths(
                    in_type, out_type, sub_class=sub_class, protocol=protocol
                ):
                    yield path, async_wrapper(converters)
                for p_type in self.get_check_types_by_value(
                    input_value, sub_class=sub_class
                ):
                    for path, converters in self.get_all_paths(
                        p_type, out_type, sub_class=sub_class, protocol=protocol
                    ):
                        yield path, async_wrapper(converters)

    def _apply_converters(self, input_value, converters):
        for converter in converters:
            input_value = converter(input_value)
        return input_value

    def _get_obj_type(
        self, obj, full: bool = False, depth: int = 10, max_sample: int = -1
    ):
        if full:
            return deep_type(obj)
        return get_generic_type(obj)

    def convert(
        self,
        input_value,
        out_type: Type[Out],
        sub_class: bool = False,
        protocol: bool = False,
        debug: bool = False,
    ) -> Out:
        input_type = self._get_obj_type(input_value, full=True)
        for sub_input_type in iter_deep_type(input_type):
            all_converters = self.get_converter(
                sub_input_type,  # type: ignore
                out_type,
                sub_class=sub_class,
                protocol=protocol,
                input_value=input_value,
            )
            if all_converters is not None:
                for path, converter in all_converters:
                    try:
                        if debug:
                            print(
                                f"Converting {sub_input_type} to {out_type} using {path}, {converter}"
                            )
                        return converter(input_value)
                    except Exception:
                        ...
        if is_structural_type(input_type) and is_structural_type(out_type):
            in_origin = get_origin(input_type)
            out_origin = get_origin(out_type)
            if in_origin == out_origin:
                out_args = get_args(out_type)

                def _iter_func(item):
                    return self.convert(
                        item,
                        out_args[0],
                        sub_class=sub_class,
                        protocol=protocol,
                        debug=debug,
                    )

                def __iter_func_dict(item):
                    k, v = item
                    return self.convert(
                        k,
                        out_args[0],
                        sub_class=sub_class,
                        protocol=protocol,
                        debug=debug,
                    ), self.convert(
                        v,
                        out_args[1],
                        sub_class=sub_class,
                        protocol=protocol,
                        debug=debug,
                    )

                if in_origin == list or out_origin == List:
                    res = list(map(_iter_func, input_value))
                elif in_origin == tuple or out_origin == Tuple:
                    res = tuple(map(_iter_func, input_value))
                elif in_origin == set or out_origin == Set:
                    res = set(map(_iter_func, input_value))
                elif out_origin in (Iterable, Iterator):
                    res = map(_iter_func, input_value)
                elif in_origin == dict or out_origin == Dict:
                    res = dict(map(__iter_func_dict, input_value.items()))
                elif out_origin in (Mapping, MutableMapping):
                    res = dict(map(__iter_func_dict, input_value.items()))
                else:
                    raise ValueError(
                        f"Unsupported structural_type {input_type} to {out_type}"
                    )
                return cast(Out, res)

        raise ValueError(f"No converter registered for {input_type} to {out_type}")

    async def async_convert(
        self,
        input_value,
        out_type: Type[Out],
        sub_class: bool = False,
        protocol: bool = False,
        debug: bool = False,
    ) -> Out:
        input_type = self._get_obj_type(input_value, full=True)
        for sub_input_type in iter_deep_type(input_type):
            all_converters = self.async_get_converter(
                sub_input_type,  # type: ignore
                out_type,
                sub_class=sub_class,
                protocol=protocol,
                input_value=input_value,
            )
            if all_converters is not None:
                async for path, converter in all_converters:
                    try:
                        if debug:
                            print(
                                f"Converting {sub_input_type} to {out_type} using {path}, {converter}"
                            )
                        return await converter(input_value)
                    except Exception:
                        ...
        if is_structural_type(input_type) and is_structural_type(out_type):
            in_origin = get_origin(input_type)
            out_origin = get_origin(out_type)
            if in_origin == out_origin:
                out_args = get_args(out_type)

                async def _iter_func(item):
                    return await self.async_convert(
                        item,
                        out_args[0],
                        sub_class=sub_class,
                        protocol=protocol,
                        debug=debug,
                    )

                async def __iter_func_dict(item):
                    k, v = item
                    return await self.async_convert(
                        k,
                        out_args[0],
                        sub_class=sub_class,
                        protocol=protocol,
                        debug=debug,
                    ), await self.async_convert(
                        v,
                        out_args[1],
                        sub_class=sub_class,
                        protocol=protocol,
                        debug=debug,
                    )

                if in_origin == list or out_origin == List:
                    res = await asyncio.gather(*map(_iter_func, input_value))
                elif in_origin == tuple or out_origin == Tuple:
                    res = tuple(await asyncio.gather(*map(_iter_func, input_value)))
                elif in_origin == set or out_origin == Set:
                    res = set(await asyncio.gather(*map(_iter_func, input_value)))
                elif out_origin in (Iterable, Iterator):
                    res = await asyncio.gather(*map(_iter_func, input_value))
                elif in_origin == dict or out_origin == Dict:
                    items = await asyncio.gather(
                        *map(__iter_func_dict, input_value.items())
                    )
                    res = dict(items)
                elif out_origin in (Mapping, MutableMapping):
                    items = await asyncio.gather(
                        *map(__iter_func_dict, input_value.items())
                    )
                    res = dict(items)
                else:
                    raise ValueError(
                        f"Unsupported structural_type {input_type} to {out_type}"
                    )
                return cast(Out, res)
        raise ValueError(f"No converter registered for {input_type} to {out_type}")

    def auto_convert(
        self,
        sub_class: bool = False,
        protocol: bool = False,
        ignore_error: bool = False,
        globalns: dict[str, Any] | None = None,
        localns: dict[str, Any] | None = None,
    ):
        def decorator(func: Callable[P, T]):
            sig = inspect.signature(func)
            hints = get_type_hints(
                func, include_extras=True, globalns=globalns, localns=localns
            )

            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                bound = sig.bind(*args, **kwargs)
                for name, value in bound.arguments.items():
                    if name in hints:
                        try:
                            bound.arguments[name] = self.convert(
                                value,
                                hints[name],
                                sub_class=sub_class,
                                protocol=protocol,
                            )
                        except Exception as e:
                            if ignore_error:
                                continue
                            raise e
                return func(*bound.args, **bound.kwargs)

            return wrapper

        return decorator

    def async_auto_convert(
        self,
        sub_class: bool = False,
        protocol: bool = False,
        ignore_error: bool = False,
        globalns: dict[str, Any] | None = None,
        localns: dict[str, Any] | None = None,
    ):
        def decorator(func: Callable[P, Awaitable[T]]):
            sig = inspect.signature(func)
            hints = get_type_hints(
                func, include_extras=True, globalns=globalns, localns=localns
            )

            @wraps(func)
            async def wrapper(*args, **kwargs) -> T:
                bound = sig.bind(*args, **kwargs)
                for name, value in bound.arguments.items():
                    if name in hints:
                        try:
                            bound.arguments[name] = await self.async_convert(
                                value,
                                hints[name],
                                sub_class=sub_class,
                                protocol=protocol,
                            )
                        except Exception as e:
                            if ignore_error:
                                continue
                            raise e
                return await func(*bound.args, **bound.kwargs)

            return wrapper

        return decorator

    def get_edges(self, sub_class: bool = False, protocol: bool = False):
        for edge in self.get_graph(sub_class=sub_class, protocol=protocol).edges(
            data=True
        ):
            yield edge

    def show_mermaid_graph(
        self, sub_class: bool = False, protocol: bool = False, full: bool = False
    ):
        from IPython.display import display, Markdown
        import typing

        nodes = []

        def get_name(cls):
            if type(cls) in (typing._GenericAlias, typing.GenericAlias):  # type: ignore
                return str(cls)
            elif hasattr(cls, "__name__"):
                return cls.__name__
            return str(cls)

        def get_node_name(cls):
            return f"node{nodes.index(cls)}"

        text = "```mermaid\ngraph TD;\n"
        for edge in self.get_graph(
            sub_class=sub_class, protocol=protocol, combos=[self.qG] if full else None
        ).edges(data=True):
            if edge[0] not in nodes:
                nodes.append(edge[0])
            if edge[1] not in nodes:
                nodes.append(edge[1])
            line_style = "--" if edge[2].get("line", False) else "-.-"
            text += f'{get_node_name(edge[0])}["{get_name(edge[0])}"] {line_style}> {get_node_name(edge[1])}["{get_name(edge[1])}"]\n'
        text += "```"

        display(Markdown(text))
        # return text

    def get_all_paths(
        self,
        in_type: Type[In],
        out_type: Type[Out],
        sub_class: bool = False,
        protocol: bool = False,
    ):
        G = self.get_graph(
            sub_class=sub_class,
            protocol=protocol,
            combos=[self._gen_graph(in_type, out_type)],
        )
        try:
            nx.has_path(G, in_type, out_type)
            res = True
        except nx.NodeNotFound:
            res = False
        if res:
            try:
                for path in nx.shortest_simple_paths(G, in_type, out_type):
                    converters = [
                        G.get_edge_data(path[i], path[i + 1])["converter"]
                        for i in range(len(path) - 1)
                    ]
                    if len(path) == 1 and len(converters) == 0:
                        yield path * 2, [lambda x: x]
                    else:
                        yield path, converters
            except nx.NetworkXNoPath:
                ...

    def get_subclass_types(self, cls: Type):
        yield from get_subclass_types(cls)

    def get_protocol_types(self, cls: Type, strict: bool = True):
        nodes = set()
        for node in list(self.pmG.nodes()):
            if node in nodes:
                continue
            nodes.add(node)
            try:
                if not check_protocol_type(cls, node, strict=strict):
                    continue
            except TypeError:
                continue
            if cls != node:
                yield node

    def get_check_types_by_value(
        self, input_value, sub_class: bool = False, protocol: bool = False
    ):
        nodes = set()
        G = self.get_graph(sub_class=sub_class, protocol=protocol)

        for edge in G.edges():
            if edge[0] in nodes:
                continue
            if get_origin(edge[0]) in (
                Iterable,
                Iterator,
                Mapping,
                MutableMapping,
                Sequence,
                MutableSequence,
            ) or is_typeddict(edge[0]):
                nodes.add(edge[0])
                try:
                    check_type(
                        input_value,
                        edge[0],
                        collection_check_strategy=CollectionCheckStrategy.ALL_ITEMS,
                    )
                except Exception:
                    continue
                yield edge[0]


class PdtConverter:
    def __init__(self):
        self.G = nx.DiGraph()
        self.sG = nx.DiGraph()
        self.tG = nx.DiGraph()
        self.qG = nx.DiGraph()

    def get_graph(self, graphs: Optional[list[nx.DiGraph]] = None):
        return nx.all.compose_all([self.G, self.sG, self.qG] + (graphs or []))

    def _gen_graph(self, in_type: Type[In], out_type: Type[Out], deep: int = 2):
        tmp_G = nx.DiGraph()
        if deep == 0:
            return tmp_G

        im = gen_typevar_model(in_type)
        om = gen_typevar_model(out_type)

        def _gen_sub_graph(mapping, node):
            for su, sv, sc in get_connected_subgraph(self.tG, node).edges(data=True):
                tmp_G.add_edge(su.get_instance(mapping), sv.get_instance(mapping), **sc)

        for u, v, c in self.tG.edges(data=True):
            um = gen_typevar_model(u)
            vm = gen_typevar_model(v)
            combos = [(um, im), (vm, im), (um, om), (vm, om)]
            for t, i in combos:
                try:
                    mapping = extract_typevar_mapping(t, i)
                    tmp_G.add_edge(
                        um.get_instance(mapping), vm.get_instance(mapping), **c
                    )
                    _gen_sub_graph(mapping, t)
                except Exception:
                    ...
        for u, v, c in tmp_G.edges(data=True):
            tmp_G = nx.compose(tmp_G, self._gen_graph(u, v, deep - 1))

        self.qG = nx.compose(self.qG, tmp_G)
        return tmp_G

    def _gen_edge(
        self, in_type: Type[In], out_type: Type[Out], converter: Callable[P, Out]
    ):
        edges = []

        for node in self.get_graph().nodes():
            group = [
                (in_type, node),
                (out_type, node),
                (node, in_type),
                (node, out_type),
            ]
            for u, v in group:
                if u == v:
                    continue
                if self.like_issubclass(u, v):
                    edges.append((u, v, {"converter": lambda x: x, "line": False}))

        self.G.add_edge(in_type, out_type, converter=converter, line=True)

        for u, v, d in edges:
            self.sG.add_edge(u, v, **d)

    def register_generic_converter(self, input_type: Type, out_type: Type):
        def decorator(func: Callable[P, T]):
            self.tG.add_edge(input_type, out_type, converter=func)
            return func

        return decorator

    def register_converter(self, input_type: Type[In], out_type: Type[Out]):
        def decorator(func: Callable[P, T]) -> Callable[P, Out]:
            self._gen_edge(input_type, out_type, func)
            return cast(Callable[P, Out], func)

        return decorator

    def async_register_converter(self, input_type: Type[In], out_type: Type[Out]):
        def decorator(func: Callable[P, Awaitable[Out]]):
            self._gen_edge(input_type, out_type, func)
            return func

        return decorator

    def can_convert(self, in_type: Type[In], out_type: Type[Out]) -> bool:
        try:
            nx.has_path(self.get_graph(), in_type, out_type)
            res = True
        except (nx.NodeNotFound, nx.NetworkXNoPath):
            res = False
        return res

    def get_converter(self, in_type: Type[In], out_type: Type[Out]):
        G = self.get_graph()
        if self.can_convert(in_type, out_type):
            try:
                for path in nx.shortest_simple_paths(G, in_type, out_type):
                    converters = [
                        G.get_edge_data(path[i], path[i + 1])["converter"]
                        for i in range(len(path) - 1)
                    ]
                    if len(path) == 1 and len(converters) == 0:
                        path, converters = path * 2, [lambda x: x]
                    func = reduce(lambda f, g: lambda x: g(f(x)), converters)
                    yield path, func
            except nx.NetworkXNoPath:
                ...

    async def async_get_converter(self, in_type: Type[In], out_type: Type[Out]):
        def async_wrapper(converters):
            async def async_converter(input_value):
                for converter in converters:
                    if inspect.iscoroutinefunction(converter):
                        input_value = await converter(input_value)
                    else:
                        input_value = converter(input_value)
                return input_value

            return async_converter

        G = self.get_graph()
        if self.can_convert(in_type, out_type):
            try:
                for path in nx.shortest_simple_paths(G, in_type, out_type):
                    converters = [
                        G.get_edge_data(path[i], path[i + 1])["converter"]
                        for i in range(len(path) - 1)
                    ]
                    if len(path) == 1 and len(converters) == 0:
                        path, converters = path * 2, [lambda x: x]
                    yield path, async_wrapper(converters)
            except nx.NetworkXNoPath:
                ...

    def convert(
        self, input_value, out_type: Type[Out], debug: bool = False, depth: int = 3
    ) -> Out:
        input_type = deep_type(input_value)
        for source, target in self.iter_all_paths(input_value, out_type, depth=depth):
            for path, func in self.get_converter(source, target):
                if debug:
                    print(f"Converting {source} to {target} using {path}, {func}")
                try:
                    return func(input_value)
                except Exception:
                    ...
        if is_structural_type(input_type) and is_structural_type(out_type):
            in_origin = get_origin(input_type)
            out_origin = get_origin(out_type)
            if self.like_issubclass(in_origin, out_origin):  # type: ignore
                out_args = get_args(out_type)

                def _iter_func(item):
                    return self.convert(
                        item,
                        out_args[0],
                        debug=debug,
                    )

                def __iter_func_dict(item):
                    k, v = item
                    return self.convert(
                        k,
                        out_args[0],
                        debug=debug,
                    ), self.convert(
                        v,
                        out_args[1],
                        debug=debug,
                    )

                if self.like_issubclass(in_origin, list):
                    res = list(map(_iter_func, input_value))
                elif self.like_issubclass(in_origin, tuple):
                    res = tuple(map(_iter_func, input_value))
                elif self.like_issubclass(in_origin, set):
                    res = set(map(_iter_func, input_value))
                elif self.like_issubclass(in_origin, Mapping):
                    res = dict(map(__iter_func_dict, input_value.items()))
                elif self.like_issubclass(out_origin, Iterable):
                    res = list(map(_iter_func, input_value))
                else:
                    raise ValueError(
                        f"Unsupported structural_type {input_type} to {out_type}"
                    )
                return cast(Out, res)

        raise ValueError(f"No converter registered for {input_type} to {out_type}")

    async def async_convert(
        self, input_value, out_type: Type[Out], debug: bool = False, depth: int = 3
    ) -> Out:
        input_type = deep_type(input_value)
        for source, target in self.iter_all_paths(input_value, out_type, depth=depth):
            async for path, func in self.async_get_converter(source, target):
                if debug:
                    print(f"Converting {source} to {target} using {path}, {func}")
                try:
                    return await func(input_value)
                except Exception as e:
                    if debug:
                        print(e)
        if is_structural_type(input_type) and is_structural_type(out_type):
            in_origin = get_origin(input_type)
            out_origin = get_origin(out_type)
            if self.like_issubclass(in_origin, out_origin):  # type: ignore
                out_args = get_args(out_type)

                async def _iter_func(item):
                    return await self.async_convert(
                        item,
                        out_args[0],
                        debug=debug,
                    )

                async def __iter_func_dict(item):
                    k, v = item
                    return await self.async_convert(
                        k,
                        out_args[0],
                        debug=debug,
                    ), await self.async_convert(
                        v,
                        out_args[1],
                        debug=debug,
                    )

                if self.like_issubclass(in_origin, list):
                    res = await asyncio.gather(*map(_iter_func, input_value))
                elif self.like_issubclass(in_origin, tuple):
                    res = tuple(await asyncio.gather(*map(_iter_func, input_value)))
                elif self.like_issubclass(in_origin, set):
                    res = set(await asyncio.gather(*map(_iter_func, input_value)))
                elif self.like_issubclass(in_origin, Mapping):
                    items = map(__iter_func_dict, input_value.items())
                    res = dict(await asyncio.gather(*items))
                elif self.like_issubclass(out_origin, Iterable):
                    res = await asyncio.gather(*map(_iter_func, input_value))
                else:
                    raise ValueError(
                        f"Unsupported structural_type {input_type} to {out_type}"
                    )
                return cast(Out, res)

        raise ValueError(f"No converter registered for {input_type} to {out_type}")

    def auto_convert(
        self,
        ignore_error: bool = False,
        localns: dict[str, Any] | None = None,
        globalns: dict[str, Any] | None = None,
    ):
        def decorator(func: Callable[P, T]):
            sig = inspect.signature(func)
            hints = get_type_hints(
                func, include_extras=True, globalns=globalns, localns=localns
            )

            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                bound = sig.bind(*args, **kwargs)
                for name, value in bound.arguments.items():
                    if name in hints:
                        try:
                            bound.arguments[name] = self.convert(
                                value,
                                hints[name],
                            )
                        except Exception as e:
                            if ignore_error:
                                continue
                            raise e
                return func(*bound.args, **bound.kwargs)

            return wrapper

        return decorator

    def async_auto_convert(
        self,
        ignore_error: bool = False,
        localns: dict[str, Any] | None = None,
        globalns: dict[str, Any] | None = None,
    ):
        def decorator(func: Callable[P, Awaitable[T]]):
            sig = inspect.signature(func)
            hints = get_type_hints(
                func, include_extras=True, globalns=globalns, localns=localns
            )

            @wraps(func)
            async def wrapper(*args, **kwargs) -> T:
                bound = sig.bind(*args, **kwargs)
                for name, value in bound.arguments.items():
                    if name in hints:
                        try:
                            bound.arguments[name] = await self.async_convert(
                                value,
                                hints[name],
                            )
                        except Exception as e:
                            if ignore_error:
                                continue
                            raise e
                return await func(*bound.args, **bound.kwargs)

            return wrapper

        return decorator

    def show_mermaid_graph(self, graph: Optional[nx.DiGraph] = None):
        from IPython.display import display, Markdown
        import typing

        nodes = []

        def get_name(cls):
            if get_origin(cls) in (typing.Annotated,):
                return str(cls)
            if type(cls) in (typing._GenericAlias, typing.GenericAlias):  # type: ignore
                return str(cls)
            elif hasattr(cls, "__name__"):
                return cls.__name__
            return str(cls)

        def get_node_name(cls):
            return f"node{nodes.index(cls)}"

        text = "```mermaid\ngraph TD;\n"
        for edge in (
            self.get_graph().edges(data=True)
            if graph is None
            else graph.edges(data=True)
        ):
            if edge[0] not in nodes:
                nodes.append(edge[0])
            if edge[1] not in nodes:
                nodes.append(edge[1])
            line_style = "--" if edge[2].get("line", False) else "-.-"
            text += f'{get_node_name(edge[0])}["{get_name(edge[0])}"] {line_style}> {get_node_name(edge[1])}["{get_name(edge[1])}"]\n'
        text += "```"
        print(text)
        display(Markdown(text))

    def iter_all_paths(self, in_value, out_type: Type[Out], depth: int = 3):
        if depth == 0:
            return

        self.check_connected()
        paths = self.iter_basis_paths(in_value, out_type)
        if paths:
            for source, target in paths:
                yield source, target
            return

        self.iter_generic_paths(in_value, out_type, depth)

        yield from self.iter_all_paths(in_value, out_type, depth - 1)

    def iter_generic_paths(self, in_value, out_type: Type[Out], depth: int = 3):
        if depth == 0:
            return

        for u, v, c in self.tG.edges(data=True):
            um = gen_typevar_model(u)
            vm = gen_typevar_model(v)
            combos = [(um, out_type), (vm, out_type)]
            for t, i in combos:
                try:
                    mapping = extract_typevar_mapping(t, i)
                    if mapping:
                        new_in, new_out = (
                            um.get_instance(mapping),
                            vm.get_instance(mapping),
                        )
                        self.qG.add_edge(new_in, new_out, **c)
                        self.iter_generic_paths(in_value, new_in, depth - 1)  # type: ignore
                except Exception:
                    ...

    def iter_basis_paths(self, in_value, out_type: Type[Out]):
        source, target = set(), set()
        in_type = deep_type(in_value)
        for node in self.get_graph().nodes():
            if self.like_isinstance(in_value, node):
                source.add(node)
            if self.like_issubclass(node, out_type):
                target.add(node)
            if self.like_issubclass(in_type, node):
                source.add(node)
        return list(itertools.product(source, target))

    def check_connected(self, graphs: Optional[list[nx.DiGraph]] = None):
        G = self.get_graph(graphs)
        nodes = list(G.nodes())
        for source, target in itertools.combinations(nodes, 2):
            if self.like_issubclass(source, target):
                self.sG.add_edge(source, target, line=False, converter=lambda x: x)

    def like_issubclass(self, obj, cls: Type):
        return check_typevar_model(obj, cls)

    def like_isinstance(self, obj, cls: Type):
        return like_isinstance(obj, cls)
