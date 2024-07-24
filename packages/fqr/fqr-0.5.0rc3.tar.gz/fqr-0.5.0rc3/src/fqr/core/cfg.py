"""Core constants."""

__all__ = (
    'Constants',
    )

from . import lib

if lib.t.TYPE_CHECKING:  # pragma: no cover
    from . import typ


class Constants:
    """Constant values shared across all of fqr."""

    PACAKGE = 'fqr'
    """Reference to package name."""

    CLASS_AS_DICT: 'typ.string[typ.snake_case]' = 'class_as_dict'
    """Common string reference."""

    DELIM = '-'
    """Common delimiter used throughout package."""

    INDENT = int(lib.os.getenv('INDENT', 2))
    """
    Default, package-wide indentation.

    ---

    Used for `__repr__`, log messages, etc.

    """

    UNDEFINED = f'[[{PACAKGE.upper()}_DEFAULT_PLACEHOLDER]]'
    """Placeholder for undefined values that should not be `None`."""

    DELIM_REBASE = '_X_'

    __ANNOTATIONS__: 'typ.string[typ.snake_case]' = '__annotations__'
    __DATACLASS_FIELDS__: 'typ.string[typ.snake_case]' = '__dataclass_fields__'
    __DICT__: 'typ.string[typ.snake_case]' = '__dict__'
    __HERITAGE__: 'typ.string[typ.snake_case]' = '__heritage__'
    __SLOTS__: 'typ.string[typ.snake_case]' = '__slots__'
    __MODULE__: 'typ.string[typ.snake_case]' = '__module__'

    FIELDS: 'typ.string[typ.snake_case]' = 'fields'
    ENUMERATIONS: 'typ.string[typ.snake_case]' = 'enumerations'
    HASH_FIELDS: 'typ.string[typ.snake_case]' = 'hash_fields'
