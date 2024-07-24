"""Typing objects."""

__all__ = (
    'ArrayProto',
    'FieldPattern',
    'MappingProto',
    'MetaLike',
    'ObjectLike',
    'SupportsAnnotations',
    'SupportsParams',
    'VariadicArrayProto',
    'WrapperPattern',
    )

from .. import typ

from . import cns
from . import lib


class Constants(cns.Constants):
    """Constant values specific to this file."""


FieldPattern = lib.re.compile(
    r'(fqr(\.[a-zA-Z]+)*\.)?Field\[((\[)?[\.\|\,a-zA-Z0-9_ ]+(\])?)+\]'
    )

WrapperPattern = lib.re.compile(
    r'([a-zA-Z]+\.?)?(Annotated|ClassVar|Final|InitVar)'
    r'\[((\[)?[\.\|\,a-zA-Z0-9_ ]+(\])?)+\]'
    )


class ArrayProto(lib.t.Protocol, lib.t.Collection[typ.AnyTypeCo]):
    """Protocol for a generic, single-parameter array."""

    def __init__(
        self,
        iterable: lib.t.Iterable[typ.AnyTypeCo],
        /
        ) -> None: ...

    def __iter__(self) -> lib.t.Iterator[typ.AnyTypeCo]: ...


class VariadicArrayProto(
    ArrayProto[tuple[lib.Unpack[typ.ArgsType]]],
    lib.t.Protocol
    ):
    """Protocol for a generic, any-parameter array."""

    def __hash__(self) -> int: ...


class MappingProto(
    lib.t.Protocol,
    lib.t.Generic[typ.AnyTypeCo, typ.AnyOtherTypeCo]
    ):
    """Protocol for a generic, double-parameter mapping."""

    def __init__(self, *args: lib.t.Any, **kwargs: lib.t.Any) -> None: ...

    def __iter__(self) -> lib.t.Iterator[typ.AnyTypeCo]: ...

    def __getitem__(
        self,
        __name: str,
        __default: lib.t.Optional[typ.AnyType] = None
        ) -> typ.AnyTypeCo | typ.AnyType: ...

    def items(self) -> lib.t.ItemsView[typ.AnyTypeCo, typ.AnyOtherTypeCo]: ...

    def keys(self) -> lib.t.KeysView[typ.AnyTypeCo]: ...

    def values(self) -> lib.t.ValuesView[typ.AnyOtherTypeCo]: ...


class SupportsAnnotations(lib.t.Protocol):
    """
    Protocol for a typed object.

    ---

    Typed objects include `dataclass`, `TypedDict`, `pydantic.Model`, \
    and both `fqr.Field` and `fqr.Object` amongst others.

    """

    __annotations__: dict[str, lib.t.Any]
    __bases__: tuple[type, ...]
    __name__: str

    def __init__(self, *args: lib.t.Any, **kwargs: lib.t.Any) -> None: ...


class SupportsParams(lib.t.Protocol, lib.t.Generic[lib.Unpack[typ.ArgsType]]):
    """Protocol for a generic with any number of parameters."""

    if lib.sys.version_info >= (3, 9):
        def __class_getitem__(
            cls,
            item: tuple[lib.Unpack[typ.ArgsType]],
            /
            ) -> lib.types.GenericAlias: ...

    __args__: tuple[lib.Unpack[typ.ArgsType]]

    def __hash__(self) -> int: ...


class MetaLike(lib.t.Protocol):
    """Meta protocol."""

    __annotations__: typ.SnakeDict
    __dataclass_fields__: lib.t.ClassVar[typ.DataClassFields]


class ObjectLike(lib.t.Protocol):
    """Object protocol."""

    __annotations__: typ.SnakeDict
    __dataclass_fields__: lib.t.ClassVar[typ.DataClassFields]

    def __contains__(self, __key: lib.t.Any, /) -> bool: ...

    def __getitem__(self, __key: lib.t.Any, /) -> lib.t.Any: ...

    def __setitem__(
        self,
        __key: str,
        __value: lib.t.Any
        ) -> lib.t.Optional[lib.Never]: ...

    def __ior__(self, other: 'ObjectLike', /) -> None: ...

    def get(
        self,
        __key: typ.AnyString,
        __default: typ.AnyType = None
        ) -> lib.t.Any | typ.AnyType: ...

    def items(
        self
        ) -> lib.t.ItemsView[typ.string[typ.snake_case], lib.t.Any]: ...

    @classmethod
    def keys(cls) -> lib.t.KeysView[typ.string[typ.snake_case]]: ...

    def pop(
        self,
        __key: str,
        /,
        __default: typ.AnyType = Constants.UNDEFINED
        ) -> typ.AnyType | lib.t.Any | lib.Never: ...

    def setdefault(
        self,
        __key: str,
        __value: lib.t.Any
        ) -> lib.t.Optional[lib.Never]: ...

    def update(self, other: 'ObjectLike', /) -> None: ...

    def values(self) -> lib.t.ValuesView[lib.t.Any]: ...

    @lib.t.overload
    def to_dict(
        self,
        camel_case: lib.t.Literal[False] = False,
        include_null: bool = True
        ) -> typ.SnakeDict: ...
    @lib.t.overload
    def to_dict(
        self,
        camel_case: lib.t.Literal[True],
        include_null: bool
        ) -> typ.CamelDict: ...
    @lib.t.overload
    def to_dict(
        self,
        camel_case: bool,
        include_null: bool
        ) -> 'typ.SnakeDict | typ.CamelDict': ...
    def to_dict(
        self,
        camel_case: bool = False,
        include_null: bool = True
        ) -> 'typ.SnakeDict | typ.CamelDict': ...
