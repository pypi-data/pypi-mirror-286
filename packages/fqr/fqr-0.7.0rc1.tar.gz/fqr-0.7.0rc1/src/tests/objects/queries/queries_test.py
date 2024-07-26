import unittest

import fqr

from ... import mocking


class TestQuery(unittest.TestCase):
    """Fixture for testing the object."""

    def setUp(self) -> None:
        self.cls = mocking.Derivative
        return super().setUp()

    def test_01_eq(self):
        """Test __eq__."""

        self.assertIsInstance(
            self.cls.str_field == 'abc',
            fqr.objects.queries.EqQueryCondition
            )

    def test_02_ne(self):
        """Test __ne__."""

        self.assertIsInstance(
            self.cls.bool_field != True,  # noqa: E712
            fqr.objects.queries.NeQueryCondition
            )

    def test_03_le(self):
        """Test __le__."""

        self.assertIsInstance(
            self.cls.int_field <= 1,
            fqr.objects.queries.LeQueryCondition
            )

    def test_04_lt(self):
        """Test __lt__."""

        self.assertIsInstance(
            self.cls.int_field < 1,
            fqr.objects.queries.LtQueryCondition
            )

    def test_05_ge(self):
        """Test __ge__."""

        self.assertIsInstance(
            self.cls.int_field >= 1,
            fqr.objects.queries.GeQueryCondition
            )

    def test_06_gt(self):
        """Test __gt__."""

        self.assertIsInstance(
            self.cls.int_field > 1,
            fqr.objects.queries.GtQueryCondition
            )

    def test_07_contains(self):
        """Test __lshift__."""

        self.assertIsInstance(
            self.cls.str_field << 't',
            fqr.objects.queries.ContainsQueryCondition
            )

    def test_08_contains_error(self):
        """Test __lshift__ error."""

        self.assertRaises(
            fqr.objects.exc.InvalidContainerComparisonTypeError,
            lambda: self.cls.int_field << 't',
            )

    def test_09_similar(self):
        """Test __mod__."""

        self.assertIsInstance(
            self.cls.str_field % 't',
            fqr.objects.queries.SimilarQueryCondition
            )

    def test_10_similar_with_threshold(self):
        """Test __mod__ with threshold."""

        self.assertEqual(
            self.cls.str_field % ('t', 0.75),
            fqr.objects.queries.SimilarQueryCondition(
                field=self.cls.str_field.name,
                like='t',
                threshold=0.75
                )
            )

    def test_11_and_query(self):
        """Test __and__."""

        self.assertEqual(
            (
                (self.cls.int_field >= 1)
                & (self.cls.int_field < 10)
                ),
            fqr.objects.queries.AndQuery(
                and_=[
                    self.cls.int_field >= 1,
                    self.cls.int_field < 10
                    ]
                )
            )

    def test_12_or_query(self):
        """Test __or__."""

        self.assertEqual(
            (
                (self.cls.int_field >= 1)
                | (self.cls.int_field < 10)
                ),
            fqr.objects.queries.OrQuery(
                or_=[
                    self.cls.int_field >= 1,
                    self.cls.int_field < 10
                    ]
                )
            )

    def test_13_invert_query(self):
        """Test __invert__."""

        self.assertEqual(
            ~(_q := self.cls.int_field >= 1),
            fqr.objects.queries.InvertQuery(invert=_q)
            )

    def test_14_sort_asc_query(self):
        """Test __iadd__."""

        q = self.cls.int_field >= 1
        q += self.cls.int_field.name
        self.assertEqual(
            q.sorting[0],
            fqr.objects.queries.QuerySortBy(
                field=self.cls.int_field.name,
                direction='asc'
                )
            )

    def test_15_sort_desc_query(self):
        """Test __isub__."""

        q = self.cls.int_field >= 1
        q -= self.cls.int_field.name
        self.assertEqual(
            q.sorting[0],
            fqr.objects.queries.QuerySortBy(
                field=self.cls.int_field.name,
                direction='desc'
                )
            )

    def test_16_similar_without_threshold(self):
        """Test __mod__ without threshold."""

        self.assertEqual(
            self.cls.str_field % ('t', 'test'),
            fqr.objects.queries.SimilarQueryCondition(
                field=self.cls.str_field.name,
                like='t',
                threshold=fqr.objects.enm.MatchThreshold.default.value
                )
            )
