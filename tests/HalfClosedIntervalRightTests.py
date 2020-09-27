import unittest
import datetime
from intervals import HalfClosedIntervalRight


class HalfClosedIntervalRightTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.interval = HalfClosedIntervalRight(2, 9)
        self.date_interval = HalfClosedIntervalRight(datetime.date(2019, 2, 7),
                                                     datetime.date(2019, 2, 14))
        self.datetime_interval = HalfClosedIntervalRight(datetime.datetime(2019, 2, 7, 11, 30),
                                                         datetime.datetime(2019, 2, 7, 12, 30))

    def test_membership(self):
        self.assertTrue(5 in self.interval)

    def test_membership_lower(self):
        self.assertTrue(2 not in self.interval)

    def test_membership_upper(self):
        self.assertTrue(9 in self.interval)

    def test_outside_of_upperend(self):
        self.assertTrue(10 not in self.interval)

    def test_date_membership(self):
        self.assertTrue(datetime.date(2019, 2, 9) in self.date_interval)

    def test_date_membership_lowerend(self):
        self.assertTrue(datetime.date(2019, 2, 7) not in self.date_interval)

    def test_date_membership_upperend(self):
        self.assertTrue(datetime.date(2019, 2, 14)  in self.date_interval)

    def test_datetime_membership(self):
        self.assertTrue(datetime.datetime(2019, 2, 7, 11, 45) in self.datetime_interval)

    def test_datetime_membership_lowerend(self):
        self.assertTrue(datetime.datetime(2019, 2, 7, 11, 30) not in self.datetime_interval)

    def test_datetime_membership_upperend(self):
        self.assertTrue(datetime.datetime(2019, 2, 7, 12, 30)  in self.datetime_interval)


if __name__ == '__main__':
    unittest.main()
