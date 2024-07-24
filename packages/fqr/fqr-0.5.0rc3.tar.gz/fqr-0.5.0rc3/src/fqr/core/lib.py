"""Core imports."""

__all__ = (
    'argparse',
    'dataclasses',
    'datetime',
    'decimal',
    'enum',
    'functools',
    'itertools',
    'json',
    'os',
    're',
    'sys',
    't',
    'types',
    'urllib',
    'Never',
    'Self',
    'TypeVarTuple',
    'Unpack',
    )

import argparse
import dataclasses
import datetime
import decimal
import enum
import functools
import itertools
import json
import os
import re
import sys
import typing as t
import types
import urllib.parse

if sys.version_info < (3, 11):  # pragma: no cover
    from typing_extensions import Never, Self, TypeVarTuple, Unpack  # noqa  # type: ignore
else:  # pragma: no cover
    from typing import Never, Self, TypeVarTuple, Unpack
