"""Core typing."""

__all__ = (
    'camelCase',
    'datetime',
    'numeric',
    'snake_case',
    'string',
    'AnyDict',
    'AnyField',
    'AnyOtherType',
    'AnyOtherTypeCo',
    'AnyString',
    'AnyType',
    'AnyTypeCo',
    'ArgsType',
    'CamelDict',
    'Casing',
    'DataClassFields',
    'Enum',
    'FieldsTuple',
    'Literal',
    'NoneType',
    'Object',
    'ObjectType',
    'OptionalAnyDict',
    'Primitive',
    'PackageExceptionType',
    'Serial',
    'SnakeDict',
    'StringFormat',
    'StringType',
    )

from . import lib

if lib.t.TYPE_CHECKING:  # pragma: no cover
    from .. import objects  # noqa: F401
    from . import exc  # noqa: F401
    from . import typings  # noqa: F401

camelCase = lib.t.NewType('camelCase', str)
snake_case = lib.t.NewType('snake_case', str)
datetime = lib.t.NewType('datetime', str)
numeric = lib.t.NewType('numeric', str)

AnyDict = dict[str, lib.t.Any]
AnyField: lib.t.TypeAlias = 'objects.Field[AnyType]'
AnyString: lib.t.TypeAlias = lib.t.Union[str, 'string[StringType]']
CamelDict: lib.t.TypeAlias = 'dict[string[camelCase], lib.t.Any]'
Casing = (
    camelCase
    | snake_case
    )
DataClassFields: lib.t.TypeAlias = 'dict[string[snake_case], AnyField[lib.t.Any]]'  # noqa
Enum: lib.t.TypeAlias = lib.t.Union[
    'typings.typ.Array[typings.typ.Immutable]',
    lib.enum.EnumMeta
    ]
Field: lib.t.TypeAlias = 'objects.Field'
FieldsTuple: lib.t.TypeAlias = 'tuple[string[snake_case], ...]'
Literal = lib.t.Literal['*']
NoneType = lib.types.NoneType  # type: ignore[valid-type]
Object: lib.t.TypeAlias = 'objects.Object'
OptionalAnyDict = lib.t.Optional[dict[str, lib.t.Any]]
Primitive = bool | float | int | NoneType | str
Serial = Primitive | dict[Primitive, 'Serial'] | list['Serial']
SnakeDict: lib.t.TypeAlias = 'dict[string[snake_case], lib.t.Any]'
StringFormat = (
    camelCase
    | snake_case
    | datetime
    | numeric
    )

AnyType = lib.t.TypeVar('AnyType')
AnyOtherType = lib.t.TypeVar('AnyOtherType')
AnyTypeCo = lib.t.TypeVar('AnyTypeCo', covariant=True)
AnyOtherTypeCo = lib.t.TypeVar('AnyOtherTypeCo', covariant=True)
ArgsType = lib.TypeVarTuple('ArgsType')
ObjectType = lib.t.TypeVar('ObjectType', bound=Object)
StringType = lib.t.TypeVar('StringType', bound=StringFormat)

PackageExceptionType = lib.t.TypeVar(
    'PackageExceptionType',
    bound='exc.BasePackageException',
    covariant=True,
    )


class string(str, lib.t.Generic[StringType]):
    """Protocol for a generic `str`."""
