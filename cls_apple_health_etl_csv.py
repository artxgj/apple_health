from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, Optional, Union

import csv

from cls_apple_health_xml_streams import *
from cls_healthkit import HK_APPLE_DATE_FORMAT
from utils import workout_element_to_dict, element_to_dict, localize_dates_health_data, \
    between_dates_predicate, is_device_watch

import constants_apple_health_data as hd


class AppleHealthDataETLCsv(ABC):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]] = datetime(1970, 1, 1),
                 end_date: Optional[Union[str, datetime]] = datetime.now(),
                 watch_data_only: bool = False):

        self._xml_filepath: str = xml_filepath
        self._csv_filepath: str = csv_filepath
        self._watch_data_only = watch_data_only

        if start_date is None:
            self._start_date = datetime(1970, 1, 1)
        elif isinstance(start_date, str):
            self._start_date: datetime = datetime.strptime(start_date, HK_APPLE_DATE_FORMAT)
        elif isinstance(start_date, datetime):
            self._start_date: datetime = start_date
        else:
            raise TypeError(f"start_date must be a string or datetime.datetime object")

        if end_date is None:
            self._end_date = datetime.now()
        elif isinstance(end_date, str):
            self._end_date: datetime = datetime.strptime(end_date, HK_APPLE_DATE_FORMAT) + \
                             timedelta(days=1) - timedelta(seconds=1)
        elif isinstance(end_date, datetime):
            self._end_date: datetime = end_date
        else:
            raise TypeError(f"end_date must be a string or a datetime.datetime object")

        if self._end_date < self._start_date:
            raise ValueError(f"start_date {start_date} > end_date {end_date}")

        self._date_boundaries_predicate = between_dates_predicate(self._start_date, self._end_date)

    def __str__(self):
        return f"xml_filepath={self._xml_filepath}; " \
               f"csv_filepath={self._csv_filepath}; " \
               f"start_date={self._start_date}; " \
               f"end_date={self._end_date}; " \
               f"watch_data_only={self._watch_data_only}"

    @abstractmethod
    def transform(self) -> Iterator[Dict[str, Any]]:
        pass

    @abstractmethod
    def serialize(self, sort_data: bool):
        pass


class AppleHealthWorkoutETLCsv(AppleHealthDataETLCsv):
    def transform(self) -> Iterator[Dict[str, Any]]:
        stream = AppleHealthDataWorkoutStream(self._xml_filepath)
        workout_dict = map(workout_element_to_dict, stream)
        localized_workout_dict = map(localize_dates_health_data, workout_dict)

        dates_bounded_workouts = filter(lambda row: self._date_boundaries_predicate(row[hd.FIELD_START_DATE]),
                                        localized_workout_dict)

        device_filtered_workouts = filter(lambda row: is_device_watch(row[hd.FIELD_DEVICE]), dates_bounded_workouts) \
            if self._watch_data_only else dates_bounded_workouts

        return device_filtered_workouts

    def serialize(self, sort_data: bool = False):
        with open(self._csv_filepath, 'w', encoding='utf-8') as outf:
            wrtr = csv.DictWriter(outf, fieldnames=hd.Fieldnames_Workout_Csv)
            wrtr.writeheader()
            workouts = self.transform()

            if sort_data:
                workouts = iter(sorted(workouts, key=lambda row: row[hd.FIELD_START_DATE]))

            for row in workouts:
                wrtr.writerow(row)


class AppleHealthActivitySummaryETLCsv(AppleHealthDataETLCsv):
    def transform(self) -> Iterator[Dict[str, str]]:
        stream = AppleHealthDataActivitySummaryStream(self._xml_filepath)
        activity_summary_dict = map(element_to_dict, stream)

        dates_bounded_active_summaries = filter(
            lambda row: self._date_boundaries_predicate(datetime.strptime(row[hd.FIELD_DATE], HK_APPLE_DATE_FORMAT)),
            activity_summary_dict)

        return dates_bounded_active_summaries

    def serialize(self, sort_data: bool):
        with open(self._csv_filepath, 'w', encoding='utf-8') as outf:
            wrtr = csv.DictWriter(outf, fieldnames=hd.Fieldnames_ActivitySummary)
            wrtr.writeheader()

            # sort_data flag is ignored because the Activity Summary data
            # appear to be in sorted order in the xml file
            for row in self.transform():
                try:
                    wrtr.writerow(row)
                except ValueError as e:
                    print(f"* * * {e} * * * {row}")
                    print()


class AppleHealthRecordETLCsv(AppleHealthDataETLCsv):
    def __init__(self,
                 record_type: str,
                 xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(xml_filepath, csv_filepath, start_date, end_date, watch_data_only)
        self._record_type = record_type

    def transform(self) -> Iterator[Dict[str, str]]:
        record = AppleHealthDataRecordTypeStream(self._xml_filepath, self._record_type)
        record_dict = map(element_to_dict, record)
        localized_record_dict = map(localize_dates_health_data, record_dict)

        dates_bounded_records = filter(lambda row: self._date_boundaries_predicate(row[hd.FIELD_START_DATE]),
                                       localized_record_dict)

        # If a row doesn't have a device attribute, treat it as if it's a watch device
        return filter(lambda row: True if hd.FIELD_DEVICE not in row else is_device_watch(row[hd.FIELD_DEVICE]),
                      dates_bounded_records) if self._watch_data_only else dates_bounded_records

    def serialize(self, sort_data: bool = False):
        with open(self._csv_filepath, 'w', encoding='utf-8') as outf:
            wrtr = csv.DictWriter(outf, fieldnames=hd.Fieldnames_Record)
            wrtr.writeheader()
            records = self.transform()

            if sort_data:
                records = iter(sorted(records, key=lambda row: row[hd.FIELD_START_DATE]))

            for row in records:
                wrtr.writerow(row)


class AppleHealthActiveEnergyBurnedETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_ActiveEnergyBurned,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)


class AppleHealthBodyMassETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_BodyMass,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)


class AppleHealthDistanceWalkingRunningETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_DistanceWalkingRunning,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)


class AppleHealthExerciseTimeETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_AppleExerciseTime,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)


class AppleHealthRestingHeartRateETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only_data: bool = False):
        super().__init__(hd.HK_REC_TYPE_RestingHeartRate,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only_data)


class AppleHealthStepCountETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_StepCount,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)


class AppleHealthVo2MaxETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_VO2Max,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)


class AppleHealthWaist2PiR_ETLCsv(AppleHealthRecordETLCsv):
    def __init__(self, xml_filepath: str,
                 csv_filepath: str,
                 start_date: Optional[Union[str, datetime]],
                 end_date: Optional[Union[str, datetime]],
                 watch_data_only: bool = False):
        super().__init__(hd.HK_REC_TYPE_WaistCircumference,
                         xml_filepath,
                         csv_filepath,
                         start_date,
                         end_date,
                         watch_data_only)
