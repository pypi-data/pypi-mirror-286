__all__ = (
    'examples',
    'Derivative',
    'DubDeriv',
    'MixinDeriv',
    'NewDeriv',
    'TripDeriv',
    'AntiTripDeriv',
    )

import fqr

from fqr . core import lib

from . import examples


class Derivative(fqr.Object):
    """Simple test derivative."""

    secondary_key: fqr.Field[int] = 123
    str_field: fqr.Field[str] = 'abc'
    bool_field: fqr.Field[bool] = True
    int_field: fqr.Field[int] = 2
    forward_ref_alias_field: 'fqr.Field[fqr.core.typ.AnyType]' = 2
    forward_ref_union_field: 'fqr.Field[float | int | tuple[int | float, ...]]' = 2  # noqa
    forward_ref_field: fqr.Field[list['Derivative']] = []
    enumerated_bool_field: fqr.Field[bool] = fqr.Field(
        default=False,
        enum=fqr.core.enm.Boolean,
        )
    from_dict_field: fqr.Field[lib.t.Optional[str]] = {
        'default': 'asc',
        'enum': {'asc', 'desc'},
        'required': False,
        'type': lib.t.Optional[str]
        }
    null_field: fqr.Field[fqr.core.typ.NoneType] = None
    non_nullable_field: fqr.Field[int] = fqr.Field(default=4, type=int)
    required_field: fqr.Field[int]
    date_field: fqr.Field[lib.datetime.date] = (  # noqa: E731
        lambda: lib.datetime.datetime.now(lib.datetime.timezone.utc).date()
        )
    datetime_field: fqr.Field[lib.datetime.datetime] = (  # noqa: E731
        lambda: lib.datetime.datetime.now(lib.datetime.timezone.utc)
        )
    decimal_field: fqr.Field[lib.decimal.Decimal] = lib.decimal.Decimal(1e-3)
    tuple_field: fqr.Field[tuple] = (1, 2)
    generic_tuple_field: fqr.Field[tuple[str, float, bool]] = ('a', 2.5, False)  # noqa


class DubDeriv(Derivative):

    test_again: fqr.Field[bool] = True
    bob: fqr.Field[str] = 'Dan'
    other_field: fqr.Field[lib.t.Optional[str]] = fqr.Field(
        default='Paul',
        enum=['Paul'],
        type_=lib.t.Optional[str]
        )

    def do_stuff(self):
        ...


class MixinDeriv(fqr.Object):

    test_again: fqr.Field[bool] = True
    bob: fqr.Field[str] = 'David'
    other_field: fqr.Field[lib.t.Optional[str]] = fqr.Field(
        default='Albert',
        enum=['Albert'],
        type_=lib.t.Optional[str]
        )

    def do_stuff(self):
        ...


class NewDeriv(fqr.Object):

    anti_field_1: fqr.Field[str] = 'cba'
    anti_field_2: fqr.Field[bool] = False
    generic_tuple_deriv_field: fqr.Field[tuple[MixinDeriv, ...]] = lambda: (  # noqa: E731
        MixinDeriv(bob='Frank'),
        MixinDeriv(bob='Bob'),
        )


class TripDeriv(MixinDeriv, DubDeriv):

    test_another: fqr.Field[bool] = False
    new_deriv: fqr.Field[NewDeriv] = NewDeriv()
    dict_field: fqr.Field[dict] = {'record_id': 'Arnold'}
    generic_dict_field: fqr.Field[dict[str, float]] = {'record_id': 1.23}


class AntiTripDeriv(DubDeriv, MixinDeriv):

    test_another: fqr.Field[bool] = False
    new_deriv: fqr.Field[NewDeriv] = NewDeriv()
    dict_field: fqr.Field[dict] = {'record_id': 'Lauren'}
    generic_dict_field: fqr.Field[dict[str, float]] = {'record_id': 1.23}
