from typing import Any, Callable, Dict, Generator, Set, Optional, Union
from calendar import monthrange
from datetime import datetime
import csv
import re
import xml.etree.ElementTree as et


from healthkit import HK_APPLE_DATETIME_FORMAT
import healthdata as hd


__all__ = [
    'SimplePublisher',
    'between_dates_predicate',
    'date_in_month_predicate',
    'always_true',
    'is_device_watch',
    'ymd_path_str',
    'DailyAggregator',
    'localize_apple_health_datetime_str',
    'get_apple_health_metadata_entries',
    'workout_element_to_dict',
    'localize_dates_health_data',
    'element_to_dict'
]


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


class DailyAggregator:
    def __init__(self):
        self._daily_sum = {}
        self._daily_items = {}

    def clear(self):
        self._daily_sum.clear()
        self._daily_items.clear()

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


def localize_apple_health_datetime_str(dt: str):
    return datetime.strptime(dt, HK_APPLE_DATETIME_FORMAT).astimezone().strftime(HK_APPLE_DATETIME_FORMAT)


def get_apple_health_metadata_entries(elem: et.Element,
                                      key_set: Union[Set[str], str] = "all") -> Dict[str, str]:
    if key_set == "all":
        return {entry.attrib['key']: entry.attrib['value'] for entry in elem.findall('MetadataEntry')}
    else:
        return {entry.attrib["key"]: entry.attrib["value"] for entry in elem.findall('MetadataEntry')
                if entry.attrib["key"] in key_set}


def element_to_dict(elem: et.Element) -> Dict[str, str]:
    return elem.attrib.copy()


def workout_element_to_dict(elem: et.Element) -> Dict[str, str]:
    meta_row = get_apple_health_metadata_entries(elem, hd.workout_metadata_fields_set)
    elem_attrs = elem.attrib.copy()
    return {**elem_attrs, **meta_row}


def localize_dates_health_data(health_data: Dict[str, str]):
    health_data[hd.FIELD_CREATION_DATE] = localize_apple_health_datetime_str(health_data[hd.FIELD_CREATION_DATE])
    health_data[hd.FIELD_START_DATE] = localize_apple_health_datetime_str(health_data[hd.FIELD_START_DATE])
    health_data[hd.FIELD_END_DATE] = localize_apple_health_datetime_str(health_data[hd.FIELD_END_DATE])
    return health_data
