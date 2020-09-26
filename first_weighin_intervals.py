import csv
import pathlib
from typing import Any, Dict, Iterator
from utils import groupby_iterators, Interval


def weighin_date_group_key(record: Dict[str, str]) -> str:
    return record['date'][:7]


def monthly_first_weighin_dates(weighin_iter: Iterator[Dict[str, Any]]):
    for key, grouped_iter in groupby_iterators(weighin_iter, weighin_date_group_key):
        first = next(grouped_iter)
        yield first['date']


def first_weighin_intervals(weighin_iter: Iterator[Dict[str, Any]]) -> Iterator[Interval]:
    first_weighin_iter = monthly_first_weighin_dates(weighin_iter)
    left = next(first_weighin_iter)

    for right in first_weighin_iter:
        yield Interval(left, right)
        left = right
