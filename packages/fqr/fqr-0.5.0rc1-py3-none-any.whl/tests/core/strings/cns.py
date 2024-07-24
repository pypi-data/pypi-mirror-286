"""Constant values specific to module unit tests."""

__all__ = (
    'Constants',
    )

from fqr . core import strings

from .. import cns


class Constants(cns.Constants, strings.cns.Constants):
    """Constant values specific to unit tests in this module."""

    INVALID_STRING_CASING_EXAMPLE = 'WRONG_cASasdfING9000man'
