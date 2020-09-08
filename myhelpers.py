from typing import Any, Callable, Dict, Generator, Set, Optional, Union
from calendar import monthrange
from datetime import datetime
import csv

import re

import healthdata as hd
import healthkit as hk

"""
To do: rename file
"""

_re_iPhone_device = re.compile(r'.+HKDevice:.+, name:iPhone,')


def stream_to_csv(csv_path: str, fieldnames, generator: Generator[Dict[str, str], None, None], encoding: str = 'utf-8'):
    with open(csv_path, 'w', encoding=encoding) as ostream:
        wrtr = csv.DictWriter(ostream, fieldnames=fieldnames)
        wrtr.writeheader()

        for row in generator:
            wrtr.writerow(row)


def xml_to_csv_activity_summary(xml_path, csv_path):
    act_sum_elements = hd.health_elem_attrs(xml_path, hd.is_elem_activity_summary)
    stream_to_csv(csv_path, hd.Fieldnames_ActivitySummary, act_sum_elements)


def xml_to_csv_record(xml_path, csv_path):
    record_elems = hd.health_elem_attrs(xml_path, hd.is_elem_record)
    stream_to_csv(csv_path, hd.Fieldnames_Record, record_elems)


class SimplePublisher:
    def __init__(self, channels: Set[str]):
        self._channels: Dict[str, Set[Callable[[Any], Optional[Any]]]] = {channel: set() for channel in channels}

    def register(self, channel: str, callback: Callable[[Any], Optional[Any]]):
        if not callback:
            raise ValueError(f'callback is not set.')

        if channel in self._channels:
            self._channels[channel].add(callback)

    def dispatch(self, channel: str, message: Any):
        if channel in self._channels:
            for callback in self._channels[channel]:
                try:
                    callback(message)
                except Exception as e:
                    print(f'{callback} threw exception: {e}')


def inclusive_date_range(start_date: datetime, end_date: datetime) \
        -> Callable[[datetime], bool]:
    def _boolean_fn(input_date: datetime):
        return start_date <= input_date <= end_date

    return _boolean_fn


def inclusive_month_range(year: int, month: int, utc_zone: str = hk.HK_APPLE_TIMEZONE) -> Callable[[datetime], bool]:
    first_day = datetime.strptime(f'{year}-{month}-01 00:00:00 {hk.HK_APPLE_TIMEZONE}', hk.HK_APPLE_DATETIME_FORMAT)
    last_day = datetime.strptime(f'{year}-{month}-{monthrange(year, month)[1]} 23:59:59 {utc_zone}',
                                 hk.HK_APPLE_DATETIME_FORMAT)
    return inclusive_date_range(first_day, last_day)


def is_device_iphone(device: str) -> bool:
    return _re_iPhone_device.search(device) is not None


def ymd_path_str(year, month, day: Optional[int] = None):
    ym = f'{year:04}{month:02}'

    return ym if day is None else f'{ym}{day:02}'


class DailyAggregator:
    def __init__(self):
        self._daily_sum = {}
        self._daily_items = {}

    def add(self, day: datetime, value: Union[int, float]) -> None:
        key = f'{day.year:04}-{day.month:02}-{day.day:02}'

        if key not in self._daily_sum:
            self._daily_sum[key] = value
            self._daily_items[key] = 1
        else:
            self._daily_sum[key] += value
            self._daily_items[key] += 1

    @property
    def sums(self) -> Dict[str, Union[int, float]]:
        return self._daily_sum.copy()

    @property
    def averages(self) -> Dict[str, Union[int, float]]:
        return {key: val/self._daily_items[key] if self._daily_items[key] > 0 else 0.0
                for key, val in self._daily_sum.items()}
