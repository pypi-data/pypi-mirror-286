"""Typing objects."""

__all__ = (
    'string',
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

from . import cfg
from . import lib

if lib.t.TYPE_CHECKING:  # pragma: no cover
    from . import typ  # noqa: F401


class Constants(cfg.Constants):
    """Constant values specific to this file."""


# Note: these need to be here to avoid circular import.
# They are however imported by adjacent typ and injected
# to typ's __all__ for consistency.
AnyType = lib.t.TypeVar('AnyType')
AnyOtherType = lib.t.TypeVar('AnyOtherType')
AnyTypeCo = lib.t.TypeVar('AnyTypeCo', covariant=True)
AnyOtherTypeCo = lib.t.TypeVar('AnyOtherTypeCo', covariant=True)
ArgsType = lib.TypeVarTuple('ArgsType')
StringType = lib.t.TypeVar('StringType', bound='typ.StringFormat')


class ArrayProto(lib.t.Protocol, lib.t.Collection[AnyTypeCo]):
    """Protocol for a generic, single-parameter array."""

    def __init__(
        self,
        iterable: lib.t.Iterable[AnyTypeCo],
        /
        ) -> None: ...

    def __iter__(self) -> lib.t.Iterator[AnyTypeCo]: ...


class VariadicArrayProto(
    ArrayProto[tuple[lib.Unpack[ArgsType]]],
    lib.t.Protocol
    ):
    """Protocol for a generic, any-parameter array."""

    def __hash__(self) -> int: ...


class MappingProto(
    lib.t.Protocol,
    lib.t.Generic[AnyTypeCo, AnyOtherTypeCo]
    ):
    """Protocol for a generic, double-parameter mapping."""

    def __init__(self, *args: lib.t.Any, **kwargs: lib.t.Any) -> None: ...

    def __iter__(self) -> lib.t.Iterator[AnyTypeCo]: ...

    def __getitem__(
        self,
        __name: str,
        __default: lib.t.Optional[AnyType] = None
        ) -> AnyTypeCo | AnyType: ...

    def items(self) -> lib.t.ItemsView[AnyTypeCo, AnyOtherTypeCo]: ...

    def keys(self) -> lib.t.KeysView[AnyTypeCo]: ...

    def values(self) -> lib.t.ValuesView[AnyOtherTypeCo]: ...


class SupportsAnnotations(lib.t.Protocol):
    """
    Protocol for a typed object.

    ---

    Typed objects include `dataclass`, `TypedDict`, `pydantic.Model`, \
    and both `fqr.Field` and `fqr.Object` amongst others.

    """

    __annotations__: dict[str, lib.t.Any]
    __bases__: tuple[type, ...]

    def __init__(self, *args: lib.t.Any, **kwargs: lib.t.Any) -> None: ...


class SupportsParams(lib.t.Protocol, lib.t.Generic[lib.Unpack[ArgsType]]):
    """Protocol for a generic with any number of parameters."""

    if lib.sys.version_info >= (3, 9):
        def __class_getitem__(
            cls,
            item: tuple[lib.Unpack[ArgsType]],
            /
            ) -> lib.types.GenericAlias: ...

    __args__: tuple[lib.Unpack[ArgsType]]

    def __hash__(self) -> int: ...


class MetaLike(lib.t.Protocol):
    """Meta protocol."""

    __annotations__: 'typ.SnakeDict'
    __dataclass_fields__: 'lib.t.ClassVar[typ.DataClassFields]'


class ObjectLike(lib.t.Protocol):
    """Object protocol."""

    __annotations__: 'typ.SnakeDict'
    __bases__: tuple[type, ...]
    __dataclass_fields__: 'lib.t.ClassVar[typ.DataClassFields]'

    def __contains__(self, __key: lib.t.Any, /) -> bool: ...

    def __getitem__(self, __key: lib.t.Any, /) -> lib.t.Any: ...

    def __setitem__(
        self,
        __key: str,
        __value: lib.t.Any
        ) -> lib.t.Optional[lib.Never]: ...

    def __ior__(self, other: 'ObjectLike', /) -> lib.Self: ...

    def get(
        self,
        __key: 'typ.AnyString',
        __default: AnyType = None
        ) -> lib.t.Any | AnyType: ...

    def items(
        self
        ) -> 'lib.t.ItemsView[typ.string[typ.snake_case], lib.t.Any]': ...

    @classmethod
    def keys(cls) -> 'lib.t.KeysView[typ.string[typ.snake_case]]': ...

    def pop(
        self,
        __key: str,
        /,
        __default: AnyType = Constants.UNDEFINED
        ) -> AnyType | lib.t.Any | lib.Never: ...

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
        ) -> 'typ.SnakeDict': ...
    @lib.t.overload
    def to_dict(
        self,
        camel_case: lib.t.Literal[True],
        include_null: bool
        ) -> 'typ.CamelDict': ...
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


class string(str, lib.t.Generic[StringType]):
    """Generic `str` protocol."""


FieldPattern = lib.re.compile(
    r'(fqr(\.[a-zA-Z]{1,32}){0,32}\.)?Field'
    r'\[((\[)?[\.\|\,a-zA-Z0-9_ ]{1,64}(\])?){1,64}\]'
    )

WrapperPattern = lib.re.compile(
    r'([a-zA-Z]{1,64}\.?)?(Annotated|ClassVar|Final|InitVar)'
    r'\[((\[)?[\.\|\,a-zA-Z0-9_ ]{1,64}(\])?){1,64}\]'
    )
