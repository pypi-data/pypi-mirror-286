"""Typing types."""

from .. import typ

__all__ = (
    'AnyOrForwardRef',
    'Array',
    'ArrayType',
    'Immutable',
    'Mapping',
    'MappingType',
    'NumberType',
    'Typed',
    'VariadicArray',
    'VariadicArrayType',
    'StrOrForwardRef',
    'UnionGenericAlias',
    *typ.__all__
    )

from .. typ import *

from . import lib
from . import obj

AnyOrForwardRef = lib.t.ForwardRef | lib.t.Any
StrOrForwardRef = lib.t.ForwardRef | str
UnionGenericAlias = type(int | str)
Wrapper = obj.SupportsParams[lib.Unpack[ArgsType]]

Array: lib.t.TypeAlias = obj.ArrayProto[AnyType]
Immutable = (
    bool
    | bytes
    | complex
    | lib.decimal.Decimal
    | lib.enum.Enum
    | float
    | lib.fractions.Fraction
    | int
    | NoneType
    | range
    | str
    | lib.enum.EnumMeta
    | frozenset['Immutable']
    | tuple['Immutable', ...]
    | lib.types.MappingProxyType['Immutable', 'Immutable']
    )
Mapping: lib.t.TypeAlias = obj.MappingProto[AnyType, AnyOtherType]
NumberType = lib.t.TypeVar('NumberType', bound=lib.numbers.Number)
Typed = obj.SupportsAnnotations
VariadicArray: lib.t.TypeAlias = (
    obj.VariadicArrayProto[lib.Unpack[tuple[AnyType, ...]]]
    )

ArrayType = lib.t.TypeVar('ArrayType', bound=Array)
MappingType = lib.t.TypeVar('MappingType', bound=Mapping)
VariadicArrayType = lib.t.TypeVar('VariadicArrayType', bound=VariadicArray)
