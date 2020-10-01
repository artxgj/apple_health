import abc
import datetime
import itertools
from collections import namedtuple
from typing import Callable, Iterator, Optional, Sequence, Union

__all__ = [
    'IntervalTypes',
    'Interval',
    'ClosedInterval',
    'HalfClosedIntervalLeft',
    'HalfClosedIntervalRight',
    'OpenInterval',
    'map_elements_to_intervals',
    'month_firstdate_intervals',
    'ElementIntervalPair'
]

IntervalTypes = Union[int, float, str, datetime.date, datetime.datetime]


class Interval(abc.ABC):
    """
    Interval between a and b, where a < b
    """
    def __init__(self, lower_end: IntervalTypes, upper_end: IntervalTypes):
        if type(lower_end) != type(upper_end):
            raise TypeError("Types mismatch for lower_end and upper_end.")

        if lower_end >= upper_end:
            raise ValueError("lower_end must be < upper_end")

        self._a = lower_end
        self._b = upper_end

    @abc.abstractmethod
    def __contains__(self, item):
        pass

    @property
    def lower_end(self) -> IntervalTypes:
        return self._a

    @property
    def upper_end(self) -> IntervalTypes:
        return self._b


class HalfClosedIntervalLeft(Interval):
    """
    [a, b)
    """
    def __contains__(self, x: IntervalTypes) -> bool:
        """ x in [a, b) """
        return self.lower_end <= x < self.upper_end


class HalfClosedIntervalRight(Interval):
    """
    (a, b]
    """

    def __contains__(self, x: IntervalTypes) -> bool:
        """ x in (a, b] """
        return self.lower_end < x <= self.upper_end


class OpenInterval(Interval):
    """
    (a, b)
    """
    def __contains__(self, x: IntervalTypes) -> bool:
        """ x in (a, b)"""
        return self.lower_end < x < self.upper_end


class ClosedInterval(Interval):
    """
    [a, b]
    """
    def __contains__(self, x: IntervalTypes):
        return self.lower_end <= x <= self.upper_end


ElementIntervalPair = namedtuple('ElementIntervalPair', ('element', 'interval'))


def map_elements_to_intervals(sorted_elements: Iterator[IntervalTypes],
                              sorted_intervals: Sequence[Interval]) \
        -> Iterator[ElementIntervalPair]:
    try:
        elem = next(sorted_elements)
        intervals = iter(sorted_intervals)
        interval = next(intervals)

        while True:
            if elem in interval:
                yield ElementIntervalPair(elem, interval)
                elem = next(sorted_elements)
            else:
                interval = next(intervals)

    except StopIteration:
        pass


def month_firstdate_intervals(
        dates_iter: Iterator[Union[str, datetime.date]],
        keyfunc: Callable[[IntervalTypes], IntervalTypes],
        make_partial_interval_lastmonth: bool = False) \
        -> Sequence[HalfClosedIntervalLeft]:

    month_groups = itertools.groupby(dates_iter, keyfunc)
    _, lower_group = next(month_groups)
    date_intervals = []
    lower_list = list(lower_group)

    # lower endpoint's first date and last date
    lower_first, lower_last = lower_list[0], lower_list[-1]

    for _, upper_group in month_groups:
        upper_list = list(upper_group)

        # upper end point's first date and last date
        upper_first, upper_last = upper_list[0], upper_list[-1]
        date_intervals.append(HalfClosedIntervalLeft(lower_first, upper_first))
        lower_first, lower_last = upper_first, upper_last

    if make_partial_interval_lastmonth and lower_first < lower_last:
        date_intervals.append(HalfClosedIntervalLeft(lower_first, lower_last))

    return date_intervals
