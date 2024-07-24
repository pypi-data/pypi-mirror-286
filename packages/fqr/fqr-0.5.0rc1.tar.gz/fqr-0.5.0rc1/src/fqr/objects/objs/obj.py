"""Object module."""

__all__ = (
    'Object',
    )

from ... import core

from .. import cns
from .. import exc
from .. import lib
from .. import metas
from .. import typ
from .. import utl

if lib.t.TYPE_CHECKING:  # pragma: no cover
    from .. import queries


class Constants(cns.Constants):
    """Constant values specific to this file."""


@lib.dataclass_transform(
    field_specifiers=(typ.Field, )
    )
class ObjectBase(metaclass=metas.Meta):
    """Base for Objects, used for typing purposes."""

    __annotations__: typ.SnakeDict
    __dict__: dict[typ.AnyString, lib.t.Any]
    __dataclass_fields__: lib.t.ClassVar[typ.DataClassFields]
    __heritage__: lib.t.ClassVar[tuple['metas.Meta', ...]]

    enumerations: lib.t.ClassVar[dict[str, tuple[typ.Primitive, ...]]]
    fields: lib.t.ClassVar[typ.FieldsTuple]
    hash_fields: lib.t.ClassVar[typ.FieldsTuple]

    def __repr__(self) -> str:
        """
        Return constructor represented as a neatly formatted JSON string.

        """

        return core.codecs.utl.serialize(self)

    def __init__(
        self,
        class_as_dict: lib.t.Optional[dict[typ.string[typ.snake_case], lib.t.Any]] = None,
        /,
        **kwargs: lib.t.Any
        ):
        ckwargs = {
            cname: value
            for name, value
            in kwargs.items()
            if (cname := core.strings.utl.cname_for(name, self.fields))
            }

        if isinstance(class_as_dict, lib.t.Mapping):
            class_as_cdict = {
                cname: value
                for name, value
                in class_as_dict.items()
                if (cname := core.strings.utl.cname_for(name, self.fields))
                }
            ckwargs |= class_as_cdict

        for cname, field in self.__dataclass_fields__.items():
            if cname not in ckwargs:
                ckwargs[cname] = field.factory()

        for cname, value in ckwargs.items():
            setattr(self, cname, value)

        self.__post_init__()

    def __post_init__(self) -> None:
        """Method that will always run after instantiation."""

    def __delitem__(self, __key: lib.t.Any) -> lib.t.Optional[lib.Never]:
        """Reset current value for key to field default."""

        if (
            isinstance(__key, str)
            and (k := core.strings.utl.cname_for(__key, self.fields))
            ):
            self.pop(k, None)
            return None
        else:
            raise KeyError(__key)

    def __getitem__(self, __key: lib.t.Any, /) -> lib.t.Any:
        """Return field value dict style."""

        if (
            isinstance(__key, str)
            and (k := core.strings.utl.cname_for(__key, self.fields))
            ):
            value = getattr(
                self,
                k,
                (
                    field_.factory()
                    if core.typings.utl.check.is_field(
                        field_ := self.__dataclass_fields__[k]
                        )
                    else field_['default']
                    )
                )
            if (
                isinstance(value, Object)
                and (
                    callers := lib.t.cast(
                        lib.types.FrameType,
                        lib.t.cast(
                            lib.types.FrameType,
                            lib.inspect.currentframe()
                            ).f_back
                        ).f_code.co_names
                    )
                and 'dict' in callers
                and (
                    callers[0] == 'dict'
                    or (
                        callers[callers.index('dict') - 1]
                        != 'to_dict'
                        )
                    )
                ):
                return value.to_dict()
            elif (
                core.typings.utl.check.is_array(value)
                and (
                    callers := lib.t.cast(
                        lib.types.FrameType,
                        lib.t.cast(
                            lib.types.FrameType,
                            lib.inspect.currentframe()
                            ).f_back
                        ).f_code.co_names
                    )
                and 'dict' in callers
                and (
                    callers[0] == 'dict'
                    or (
                        callers[callers.index('dict') - 1]
                        != 'to_dict'
                        )
                    )
                ):
                return value.__class__(
                    item.to_dict()
                    if core.typings.utl.check.is_object(item)
                    else item
                    for item
                    in value
                    )
            elif (
                core.typings.utl.check.is_mapping(value)
                and (
                    callers := lib.t.cast(
                        lib.types.FrameType,
                        lib.t.cast(
                            lib.types.FrameType,
                            lib.inspect.currentframe()
                            ).f_back
                        ).f_code.co_names
                    )
                and 'dict' in callers
                and (
                    callers[0] == 'dict'
                    or (
                        callers[callers.index('dict') - 1]
                        != 'to_dict'
                        )
                    )
                ):
                return value.__class__(
                    {
                        (
                            k.to_dict()
                            if core.typings.utl.check.is_object(k)
                            else k
                            ): (
                                v.to_dict()
                                if core.typings.utl.check.is_object(v)
                                else v
                                )
                        for k, v
                        in value.items()
                        }
                    )
            else:
                return value
        else:
            raise KeyError(__key)

    def __setitem__(
        self,
        __key: str,
        __value: lib.t.Any
        ) -> lib.t.Optional[lib.Never]:
        """Set field value dict style."""

        if (k := core.strings.utl.cname_for(__key, self.fields)):
            setattr(self, k, __value)
            return None
        else:
            raise KeyError(__key)

    def __contains__(self, __key: lib.t.Any, /) -> bool:
        """Return `True` if `__key` is a field for self."""

        return bool(core.strings.utl.cname_for(__key, self.fields))

    def __len__(self) -> int:
        """Return count of fields."""

        return len(self.fields)

    def __hash__(self) -> int:
        return hash(
            Constants.DELIM.join(
                [
                    '.'.join((k, str(v)))
                    for k
                    in self.hash_fields
                    if (v := self.get(k))
                    ]
                )
            )

    def __bool__(self) -> bool:
        """Determine truthiness by diff with default field values."""

        return bool(self - self.__class__())

    @lib.t.overload
    def __eq__(
        self,
        other: 'typ.AnyField[lib.t.Any]'
        ) -> bool: ...
    @lib.t.overload
    def __eq__(
        self: object,
        other: object
        ) -> bool: ...
    @lib.t.overload
    def __eq__(
        self,
        other: lib.t.Any
        ) -> lib.t.Union[bool, 'queries.EqQueryCondition', lib.Never]: ...
    def __eq__(
        self,
        other: lib.t.Union[object, lib.t.Any]
        ) -> lib.t.Union[bool, 'queries.EqQueryCondition', lib.Never]:

        return hash(self) == hash(other)

    @lib.t.overload
    def __ne__(
        self,
        other: 'typ.AnyField[lib.t.Any]'
        ) -> bool: ...
    @lib.t.overload
    def __ne__(
        self: object,
        other: object
        ) -> bool: ...
    @lib.t.overload
    def __ne__(
        self,
        other: lib.t.Any
        ) -> lib.t.Union[bool, 'queries.NeQueryCondition', lib.Never]: ...
    def __ne__(
        self,
        other: lib.t.Union[object, lib.t.Any, 'typ.AnyField[lib.t.Any]']
        ) -> lib.t.Union[bool, 'queries.NeQueryCondition', lib.Never]:

        return hash(self) != hash(other)

    def __sub__(self, other: lib.Self) -> typ.SnakeDict:
        """Calculate diff between same object types."""

        diff: typ.SnakeDict = {}
        for field in self.fields:
            if self[field] != other[field]:
                diff[field] = other[field]

        return diff

    def __iter__(
        self
        ) -> lib.t.Iterator[tuple[typ.string[typ.snake_case], lib.t.Any]]:
        """
        Return an iterator of keys and values like a `dict`.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        for k, v in self.items():
            yield k, v

    @lib.t.overload
    def __lshift__(
        self,
        other: core.typings.obj.ObjectLike,
        ) -> lib.Self: ...
    @lib.t.overload
    def __lshift__(
        self,
        other: lib.t.Any,
        ) -> lib.t.Union[
            'queries.ContainsQueryCondition',
            lib.Self,
            lib.Never
            ]: ...
    def __lshift__(
        self,
        other: core.typings.obj.ObjectLike | lib.t.Any
        ) -> lib.t.Union[
            lib.Self,
            'queries.ContainsQueryCondition',
            lib.Never
            ]:
        """
        Interpolate values from other if populated with non-default \
        and return a new instance without mutating self or other.

        """

        if not all(field in other for field in self.__dataclass_fields__):
            raise exc.InvalidObjectComparisonError(self, other)
        else:
            object_ = self.__class__()
            for field, __field in self.__dataclass_fields__.items():
                default_value = __field.factory()
                if (
                    self[field] == default_value
                    and other[field] != default_value
                    ):
                    object_[field] = other[field]
                else:
                    object_[field] = self[field]
            return object_

    def __rshift__(
        self,
        other: core.typings.obj.ObjectLike
        ) -> lib.Self:
        """
        Overwrite values from other if populated with non-default \
        and return a new instance without mutating self or other.

        """

        object_ = self.__class__()
        for field, __field in self.__dataclass_fields__.items():
            if other[field] != __field.factory():
                object_[field] = other[field]
            else:
                object_[field] = self[field]
        return object_

    def __reversed__(self) -> lib.t.Iterator[typ.string[typ.snake_case]]:
        """Return a reversed iterator of keys like a `dict`."""

        for field in reversed(self.keys()):
            yield field

    def __copy__(self) -> lib.Self:
        """Return a copy of the instance."""

        return self.__class__(dict(self))

    def __deepcopy__(
        self,
        memo: lib.t.Optional[typ.AnyDict] = None
        ) -> lib.Self:
        """Return a deep copy of the instance."""

        return self.__copy__()

    def __getstate__(self) -> typ.SnakeDict:
        return dict(self)

    def __setstate__(self, state: typ.SnakeDict) -> None:
        self.update(self.__class__(state))
        return None

    def __ior__(self, other: core.typings.obj.ObjectLike, /) -> None:
        self.update(other)
        return None

    def get(
        self,
        __key: typ.AnyString,
        __default: typ.AnyType = None
        ) -> lib.t.Any | typ.AnyType:
        """Return value by key if exists, otherwise default."""

        if (k := core.strings.utl.cname_for(__key, self.fields)):
            return self[k]
        else:
            return __default

    def copy(self) -> lib.Self:
        """Return a copy of the instance."""

        return self.__copy__()

    @classmethod
    def fromkeys(
        cls,
        __keys: lib.t.Iterable[typ.string[typ.snake_case]],
        /
        ) -> lib.Self:
        """
        Return an object instance from keys like a `dict`.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        return cls()

    @classmethod
    def keys(cls) -> lib.t.KeysView[typ.string[typ.snake_case]]:
        """
        Return an iterator of keys like a `dict`.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        return lib.t.KeysView(
            {
                k.rstrip('_'): v  # type: ignore[misc]
                for k, v
                in cls.__dataclass_fields__.items()
                }
            )

    def items(self) -> lib.t.ItemsView[typ.string[typ.snake_case], lib.t.Any]:
        """
        Return an iterator of keys and values like a `dict`.

        ---

        Removes any suffixed underscores from field names (`_`).

        """

        return self.to_dict().items()

    def pop(
        self,
        __key: str,
        /,
        __default: typ.AnyType = Constants.UNDEFINED
        ) -> typ.AnyType | lib.t.Any | lib.Never:
        """Return current value for key and reset instance value to field default."""

        if (cname := core.strings.utl.cname_for(__key, self.fields)):
            value = self[cname]
            self[cname] = self.__dataclass_fields__[cname].factory()
            return value
        elif __default == Constants.UNDEFINED:
            raise KeyError
        else:
            return __default

    def setdefault(
        self,
        __key: str,
        __value: lib.t.Any
        ) -> lib.t.Optional[lib.Never]:
        """Set value for key if unset; otherwise do nothing."""

        if (
            (k := core.strings.utl.cname_for(__key, self.fields))
            and (
                (
                    _value := self.get(k, Constants.UNDEFINED)
                    ) == Constants.UNDEFINED
                or _value == self.__dataclass_fields__[k].factory()
                )
            ):
            self[k] = __value
        elif not k:
            raise KeyError

        return None

    def update(self, other: core.typings.obj.ObjectLike, /) -> None:
        """Update values like a `dict`."""

        for k, v in other.items():
            if core.strings.utl.cname_for(k, self.fields):
                self[k] = v

        return None

    def values(self) -> lib.t.ValuesView[lib.t.Any]:
        """Return an iterator of values like a `dict`."""

        return lib.t.ValuesView(dict(self))

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
        ) -> 'typ.SnakeDict | typ.CamelDict':
        """
        Same as `dict(Object)`, but gives fine-grained control over \
        casing and inclusion of `null` values.

        ---

        If specified, keys may optionally be converted to camelCase.

        `None` values may optionally be discarded as well.

        ---

        Removes any suffixed underscores from field names (`_`) and \
        recursively pops any key, value pairs prefixed with single \
        underscores (`_`).

        """

        d = {
            k: v
            for k
            in self.fields
            if (v := self[k]) is not None
            or (include_null and v is None)
            }
        as_dict: typ.SnakeDict = {}
        for key, value in d.items():
            if isinstance(value, Object):
                as_dict[key] = value.to_dict(camel_case, include_null)
            elif core.typings.utl.check.is_array(value):
                as_dict[key] = value.__class__(
                    (
                        v.to_dict(camel_case, include_null)
                        if isinstance(v, Object)
                        else v
                        for v
                        in value
                        if v is not None
                        or include_null
                        )
                    )
            elif core.typings.utl.check.is_mapping(value):
                as_dict[key] = value.__class__(
                    **{
                        (
                            core.strings.utl.snake_case_to_camel_case(k.strip('_'))
                            if (camel_case and isinstance(k, str))
                            else k
                            ): (
                                v.to_dict(camel_case, include_null)
                                if isinstance(v, Object)
                                else v
                                )
                        for k, v
                        in value.items()
                        if utl.is_public_field(k)
                        and v is not None
                        or include_null
                        }
                    )
            else:
                as_dict[key] = value

        if camel_case:
            return {
                core.strings.utl.snake_case_to_camel_case(k.strip('_')): v
                for k, v
                in as_dict.items()
                }
        else:
            snake_dict: typ.SnakeDict = {
                k.rstrip('_'): v  # type: ignore[misc]
                for k, v
                in as_dict.items()
                }
            return snake_dict


@lib.dataclass_transform(
    kw_only_default=True,
    field_specifiers=(typ.Field, )
    )
class Object(ObjectBase):
    """Object typed Object class."""

    class_as_dict: lib.t.Optional[dict[typ.string[typ.snake_case], lib.t.Any]] = None
    """
    Instantiate class directly from passed `dict` (assumed to be \
    version of class in `dict` form).

    """
