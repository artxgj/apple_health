import unittest

from intervals import Interval, HalfClosedIntervalLeft


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


if __name__ == '__main__':
    unittest.main()
