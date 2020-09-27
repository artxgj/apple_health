import unittest
import datetime
from intervals import HalfClosedIntervalLeft


class HalfClosedIntervalLeftTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.interval = HalfClosedIntervalLeft(2, 9)
        self.date_interval = HalfClosedIntervalLeft(datetime.date(2019, 2, 7),
                                                    datetime.date(2019, 2, 14))
        self.datetime_interval = HalfClosedIntervalLeft(datetime.datetime(2019, 2, 7, 11, 30),
                                                        datetime.datetime(2019, 2, 7, 12, 30))

    def test_membership(self):
        self.assertTrue(5 in self.interval)

    def test_membership_lower(self):
        self.assertTrue(2 in self.interval)

    def test_membership_upper(self):
        self.assertTrue(9 not in self.interval)

    def test_outside_of_lowerend(self):
        self.assertTrue(1 not in self.interval)

    def test_date_membership(self):
        self.assertTrue(datetime.date(2019, 2, 9) in self.date_interval)

    def test_date_membership_lowerend(self):
        self.assertTrue(datetime.date(2019, 2, 7) in self.date_interval)

    def test_date_membership_upperend(self):
        self.assertTrue(datetime.date(2019, 2, 14) not in self.date_interval)

    def test_datetime_membership(self):
        self.assertTrue(datetime.datetime(2019, 2, 7, 11, 45) in self.datetime_interval)

    def test_datetime_membership_lowerend(self):
        self.assertTrue(datetime.datetime(2019, 2, 7, 11, 30) in self.datetime_interval)

    def test_datetime_membership_upperend(self):
        self.assertTrue(datetime.datetime(2019, 2, 7, 12, 30) not in self.datetime_interval)


if __name__ == '__main__':
    unittest.main()
