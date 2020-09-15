from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Iterator, Union

import csv


from healthkit import HK_APPLE_DATE_FORMAT
from healthdata import FIELD_START_DATE, FIELD_DEVICE, Fieldnames_Workout_Csv, FIELD_DATE, Fieldnames_ActivitySummary, \
    HK_REC_TYPE_ActiveEnergyBurned, Fieldnames_Record
from utils import workout_element_to_dict, element_to_dict, localize_dates_health_data, between_dates_predicate, is_device_watch

import apple_health_xml_streams as ahxs


class AppleHealthXmlToCsv(ABC):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Union[str, datetime] = datetime(1970, 1, 1),
                 end_date: Union[str, datetime] = datetime.now() + timedelta(days=1) - timedelta(seconds=1),
                 sort_data: bool = False,
                 watch_only_data: bool = False):

        self._xml_filepath: str = xml_filepath
        self._csv_filepath: str = csv_filepath
        self._sort_data = sort_data
        self._watch_only_data = watch_only_data

        if isinstance(start_date, str):
            self._start_date: datetime = datetime.strptime(start_date, HK_APPLE_DATE_FORMAT)
        elif isinstance(start_date, datetime):
            self._start_date: datetime = start_date
        else:
            raise TypeError(f"start_date must be a string or datetime.datetime object")

        if isinstance(end_date, str):
            self._end_date: datetime = datetime.strptime(end_date, HK_APPLE_DATE_FORMAT) + \
                             timedelta(days=1) - timedelta(seconds=1)
        elif isinstance(end_date, datetime):
            self._end_date: datetime = end_date
        else:
            raise TypeError(f"end_date must be a string or datetime.datetime object")

        if self._end_date < self._start_date:
            raise ValueError(f"start_date {start_date} > end_date {end_date}")

        self._date_boundaries_predicate = between_dates_predicate(self._start_date, self._end_date)

    def __str__(self):
        return f"xml_filepath: {self._xml_filepath}; " \
               f"csv_filepath: {self._csv_filepath}; " \
               f"start_date: {self._start_date}; " \
               f"end_date: {self._end_date}; " \
               f"sort_data: {self._sort_data}; " \
               f"watch_only_data: {self._watch_only_data}\n"

    @abstractmethod
    def transform(self) -> Iterator[Dict[str, str]]:
        pass

    @abstractmethod
    def serialize(self):
        pass


class AppleHealthWorkoutXmlCsv(AppleHealthXmlToCsv):
    def transform(self) -> Iterator[Dict[str, str]]:
        wstream = ahxs.AppleHealthDataWorkoutStream(self._xml_filepath)
        workout_dict = map(workout_element_to_dict, wstream)
        localized_workout_dict = map(localize_dates_health_data, workout_dict)

        dates_bounded_workouts = filter(lambda row: self._date_boundaries_predicate(row[FIELD_START_DATE]),
                                            localized_workout_dict)

        unsorted_workouts = filter(lambda row: is_device_watch(row[FIELD_DEVICE]), dates_bounded_workouts) \
                if self._watch_only_data else dates_bounded_workouts

        if self._sort_data:
            return iter(sorted(unsorted_workouts, key=lambda row: row[FIELD_START_DATE]))
        else:
            return unsorted_workouts

    def serialize(self):
        with open(self._csv_filepath, 'w', encoding='utf-8') as outf:
            wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Workout_Csv)
            wrtr.writeheader()

            for row in self.transform():
                wrtr.writerow(row)


class AppleHealthActiveSummaryXmlCsv(AppleHealthXmlToCsv):
    def transform(self) -> Iterator[Dict[str, str]]:
        wstream = ahxs.AppleHealthDataActivitySummaryStream(self._xml_filepath)
        active_summary_dict = map(element_to_dict, wstream)

        dates_bounded_active_summaries = filter(
            lambda row: self._date_boundaries_predicate(datetime.strptime(row[FIELD_DATE], HK_APPLE_DATE_FORMAT)),
            active_summary_dict)

        return dates_bounded_active_summaries

    def serialize(self):
        with open(self._csv_filepath, 'w', encoding='utf-8') as outf:
            wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_ActivitySummary)
            wrtr.writeheader()

            for row in self.transform():
                wrtr.writerow(row)


class AppleHealthRecordXmlCsv(AppleHealthXmlToCsv):
    def __init__(self,
                 record_type: str,
                 xml_filepath: str,
                 csv_filepath: str,
                 start_date: Union[str, datetime] = datetime(1970, 1, 1),
                 end_date: Union[str, datetime] = datetime.now() + timedelta(days=1) - timedelta(seconds=1),
                 sort_data: bool = False,
                 watch_only_data: bool = False):
        super().__init__(xml_filepath, csv_filepath, start_date, end_date, sort_data, watch_only_data)
        self._record_type = record_type

    def transform(self) -> Iterator[Dict[str, str]]:
        record = ahxs.AppleHealthDataRecordTypeStream(self._xml_filepath, self._record_type)
        record_dict = map(element_to_dict, record)
        localized_record_dict = map(localize_dates_health_data, record_dict)

        dates_bounded_records = filter(lambda row: self._date_boundaries_predicate(row[FIELD_START_DATE]),
                                       localized_record_dict)

        unsorted_records = filter(lambda row: is_device_watch(row[FIELD_DEVICE]), dates_bounded_records) \
            if self._watch_only_data else dates_bounded_records

        if self._sort_data:
            return iter(sorted(unsorted_records, key=lambda row: row[FIELD_START_DATE]))
        else:
            return unsorted_records

    def serialize(self):
        with open(self._csv_filepath, 'w', encoding='utf-8') as outf:
            wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Record)
            wrtr.writeheader()

            for row in self.transform():
                wrtr.writerow(row)


class AppleHealthActiveEnergyBurnedXmlCsv(AppleHealthRecordXmlCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Union[str, datetime] = datetime(1970, 1, 1),
                 end_date: Union[str, datetime] = datetime.now() + timedelta(days=1) - timedelta(seconds=1),
                 sort_data: bool = False,
                 watch_only_data: bool = False):
        super().__init__(HK_REC_TYPE_ActiveEnergyBurned,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         sort_data,
                         watch_only_data)


