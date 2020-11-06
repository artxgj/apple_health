import unittest

from intervals import Interval, HalfClosedIntervalLeft, ClosedInterval


class IntervalTestCase(unittest.TestCase):
    def test_Interval_Instantiation(self):
        with self.assertRaises(TypeError):
            Interval(1, 3)

    def test_Interval_types_mismatch(self):
        with self.assertRaises(TypeError):
            HalfClosedIntervalLeft(1, 'a')

    def test_Interval_values_exception(self):
        with self.assertRaises(ValueError):
            HalfClosedIntervalLeft(9, 2)

    def test_Interval_equals_exception(self):
        with self.assertRaises(TypeError):
            k = HalfClosedIntervalLeft(2, 9)
            j = ClosedInterval(2, 9)
            k == j

    def test_Interval_notequals_exception(self):
        with self.assertRaises(TypeError):
            k = HalfClosedIntervalLeft(2, 9)
            j = ClosedInterval(2, 9)
            k != j

    def test_Interval_lt_exception(self):
        with self.assertRaises(TypeError):
            k = HalfClosedIntervalLeft(2, 9)
            j = ClosedInterval(2, 9)
            k < j

    def test_Interval_le_exception(self):
        with self.assertRaises(TypeError):
            k = HalfClosedIntervalLeft(2, 9)
            j = ClosedInterval(2, 9)
            k <= j

    def test_Interval_ge_exception(self):
        with self.assertRaises(TypeError):
            k = HalfClosedIntervalLeft(2, 9)
            j = ClosedInterval(2, 9)
            k >= j

    def test_Interval_gt_exception(self):
        with self.assertRaises(TypeError):
            k = HalfClosedIntervalLeft(2, 9)
            j = ClosedInterval(2, 9)
            k > j


if __name__ == '__main__':
    unittest.main()
