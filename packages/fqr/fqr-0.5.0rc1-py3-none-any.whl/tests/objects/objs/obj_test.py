"""Module objs unit tests."""

import unittest

import fqr

from fqr . core import lib

from ... import mocking

from . import cns


class Constants(cns.Constants):
    """Constant values specific to unit tests in this file."""


class TestObject(unittest.TestCase):
    """Fixture for testing `Object`."""

    def setUp(self) -> None:
        self.mcs = fqr.objects.metas.Meta
        self.cls = mocking.Derivative
        self.object_ = self.cls()
        self.trip = mocking.TripDeriv(
            str_field='123',
            )
        self.anti = mocking.AntiTripDeriv(
            str_field='321'
            )
        return super().setUp()

    def test_01_dict_functionality(self):
        """Test `Object.__getitem__()`."""

        self.assertTrue(
            self.object_['int_field']
            == self.object_.int_field
            == self.cls.int_field.default
            )

    def test_02_dict_functionality(self):
        """Test `Object.__getitem__()` raises KeyError if no key."""

        self.assertRaises(
            KeyError,
            lambda: self.object_['field_that_does_not_exist']
            )

    def test_03_iter(self):
        """Test `Object.__iter__()`."""

        self.assertEqual(dict(self.object_.__iter__()), dict(self.object_))

    def test_04_len(self):
        """Test `Object.__len__()`."""

        self.assertEqual(len(self.object_), len(self.cls.fields))

    def test_05_contains(self):
        """Test `Object.__contains__()`."""

        self.assertIn(self.object_.fields[0], self.object_)

    def test_06_ne(self):
        """Test `Object.__ne__()`."""

        self.assertFalse(self.object_ != self.object_)

    def test_07_lshift(self):
        """Test `Object.__lshift__()` correctly interpolates."""

        object_ = self.trip << self.anti
        self.assertNotEqual(object_.str_field, self.anti.str_field)

    def test_08_lshift(self):
        """Test `Object.__lshift__()` correctly interpolates."""

        object_ = self.trip << self.anti
        self.assertNotEqual(object_.other_field, self.trip.other_field)

    def test_09_rshift(self):
        """Test `Object.__rshift__()` correctly overwrites."""

        default = mocking.TripDeriv()
        object_ = self.trip >> default
        self.assertNotEqual(object_.str_field, default.str_field)

    def test_10_rshift(self):
        """Test `Object.__rshift__()` correctly overwrites."""

        object_ = self.trip >> self.anti
        self.assertEqual(object_.str_field, self.anti.str_field)

    def test_11_dict_functionality(self):
        """Test `Object.get()` returns default if no key."""

        self.assertIsNone(self.object_.get('field_that_does_not_exist'))

    def test_12_to_dict(self):
        """Test `Object.to_dict()`."""

        self.assertDictEqual(
            {
                fqr.core.strings.utl.snake_case_to_camel_case(k): self.trip[k]
                for k, v in self.trip.items()
                if type(v) in lib.t.get_args(fqr.core.typ.Primitive)
                },
            {
                k: v
                for k, v
                in self.trip.to_dict(camel_case=True).items()
                if type(v) in lib.t.get_args(fqr.core.typ.Primitive)
                }
            )

    def test_13_to_dict(self):
        """Test `Object.to_dict()`."""

        self.assertDictEqual(
            {k: v for k, v in self.object_ if v is not None},
            self.object_.to_dict(include_null=False)
            )

    def test_14_repr(self):
        """Test `Object.__repr__()`."""

        self.assertEqual(
            repr(self.trip),
            lib.json.dumps(
                dict(self.trip),
                default=fqr.core.strings.utl.convert_for_repr,
                indent=Constants.INDENT,
                sort_keys=True
                )
            )

    def tearDown(self) -> None:
        return super().tearDown()
