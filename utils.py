from calendar import monthrange
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Generator, Iterable, Iterator, Set, Optional, Union, Tuple
import csv
import itertools
import re
import xml.etree.ElementTree as et

from cls_healthkit import HK_APPLE_DATETIME_FORMAT
import constants_apple_health_data as hd


__all__ = [
    'between_dates_predicate',
    'date_in_month_predicate',
    'always_true',
    'is_device_watch',
    'ymd_path_str',
    'localize_apple_health_datetime_str',
    'get_apple_health_metadata_entries',
    'workout_element_to_dict',
    'localize_dates_health_data',
    'element_to_dict',
    'groupby_iterators',
    'Interval',
    'IntervalTypes',
    'SimplePublisher',
]


_re_iPhone_device = re.compile(r'.+HKDevice:.+, name:iPhone,')


def between_dates_predicate(start_date: datetime, end_date: datetime) \
        -> Callable[[datetime], bool]:
    """Returns a function that tests if a date is between two dates.
       Dates are converted to local timezone
    """
    if start_date > end_date:
        raise ValueError('start_date is later than end_date.')

    local_start: datetime = start_date.astimezone()
    local_end: datetime = end_date.astimezone()

    def _between_local_dates(given_date: Union[str, datetime]) -> bool:
        if isinstance(given_date, str):
            given_date = datetime.strptime(given_date, HK_APPLE_DATETIME_FORMAT)
        elif not isinstance(given_date, datetime):
            raise TypeError("date's type must be a str or datetime.datetime object.")

        return local_start <= given_date.astimezone() <= local_end
    return _between_local_dates


def date_in_month_predicate(year: int, month: int) -> Callable[[datetime], bool]:
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
    return between_dates_predicate(first_day, last_day)


def is_device_iphone(device: str) -> bool:
    return _re_iPhone_device.search(device) is not None


def is_device_watch(device: str) -> bool:
    """Apple watch can also transmit exercise data from exercise equipment, e.g., treadmill"""
    return not is_device_iphone(device)


def always_true(x: Any) -> bool:
    return True


def ymd_path_str(year, month, day: Optional[int] = None):
    ym = f'{year:04}{month:02}'

    return ym if day is None else f'{ym}{day:02}'


def localize_apple_health_datetime_str(dt: str):
    return datetime.strptime(dt, HK_APPLE_DATETIME_FORMAT).astimezone().strftime(HK_APPLE_DATETIME_FORMAT)


def localize_dates_health_data(health_data: Dict[str, str]):
    health_data[hd.FIELD_CREATION_DATE] = localize_apple_health_datetime_str(health_data[hd.FIELD_CREATION_DATE])
    health_data[hd.FIELD_START_DATE] = localize_apple_health_datetime_str(health_data[hd.FIELD_START_DATE])
    health_data[hd.FIELD_END_DATE] = localize_apple_health_datetime_str(health_data[hd.FIELD_END_DATE])
    return health_data


def element_to_dict(elem: et.Element) -> Dict[str, str]:
    return elem.attrib.copy()


def workout_element_to_dict(elem: et.Element) -> Dict[str, str]:
    meta_row = get_apple_health_metadata_entries(elem, hd.workout_metadata_fields_set)
    elem_attrs = elem.attrib.copy()
    return {**elem_attrs, **meta_row}


def groupby_iterators(input_iterator: Iterable[Dict[str, Any]], groupby_key_fn: Callable[[Any], Any]) -> \
        Tuple[Any, Iterator]:
    """Returns a 2-tuple consisting of group key and an iterator of the key's values"""
    for group_iter in itertools.groupby(input_iterator, groupby_key_fn):
        yield group_iter


def get_apple_health_metadata_entries(elem: et.Element,
                                      key_set: Union[Set[str], str] = "all") -> Dict[str, str]:
    if key_set == "all":
        return {entry.attrib['key']: entry.attrib['value'] for entry in elem.findall('MetadataEntry')}
    else:
        return {entry.attrib["key"]: entry.attrib["value"] for entry in elem.findall('MetadataEntry')
                if entry.attrib["key"] in key_set}


IntervalTypes = Union[int, float, str, datetime]


@dataclass
class Interval:
    left: IntervalTypes
    right: IntervalTypes


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


def stream_to_csv(csv_path: str, fieldnames, generator: Generator[Dict[str, str], None, None], encoding: str = 'utf-8'):
    with open(csv_path, 'w', encoding=encoding) as ostream:
        wrtr = csv.DictWriter(ostream, fieldnames=fieldnames)
        wrtr.writeheader()

        for row in generator:
            wrtr.writerow(row)

