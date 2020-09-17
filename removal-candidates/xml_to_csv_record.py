from typing import List
import csv
import datetime

from ..cls_apple_health_xml_streams import AppleHealthDataRecordTypeStream
from ..healthdata import *
from ..utils import localize_apple_health_datetime_str, localize_dates_health_data, between_dates_predicate, \
    element_to_dict, is_device_watch


def extract_record_type_history(xml_file_path: str, record_type: str) -> List[Dict[str, str]]:
    history: List[Dict[str, str]] = []

    with AppleHealthDataRecordTypeStream(xml_file_path, record_type) as record:
        for elem in record:
            replica = elem.attrib.copy()
            replica[FIELD_CREATION_DATE] = localize_apple_health_datetime_str(replica[FIELD_CREATION_DATE])
            replica[FIELD_START_DATE] = localize_apple_health_datetime_str(replica[FIELD_START_DATE])
            replica[FIELD_END_DATE] = localize_apple_health_datetime_str(replica[FIELD_END_DATE])
            history.append(replica)

    history.sort(key=lambda x: x[FIELD_START_DATE])
    return history


def write_csv(csv_filepath: str, record_type_history: List[Dict[str, str]]):
    with open(csv_filepath, 'w', encoding='utf-8') as outf:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Record)
        wrtr.writeheader()
        wrtr.writerows(record_type_history)


def xml_to_csv(xml_file_path: str,
               csv_filepath: str,
               start_date: datetime.datetime,
               end_date: datetime.datetime,
               sort_data: bool,
               watch_only_data: bool,
               record_type: str):

    with open(csv_filepath, 'w', encoding='utf-8') as outf, \
            AppleHealthDataRecordTypeStream(xml_file_path, record_type) as record:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Record)
        wrtr.writeheader()

        in_date_boundary = between_dates_predicate(start_date, end_date)
        record_dict = map(element_to_dict, record)
        localized_record_dict = map(localize_dates_health_data, record_dict)

        dates_bounded_records = filter(lambda row: in_date_boundary(row[FIELD_START_DATE]),
                                       localized_record_dict)

        unsorted_records = filter(lambda row: is_device_watch(row[FIELD_DEVICE]), dates_bounded_records) \
            if watch_only_data else dates_bounded_records

        records = sorted(unsorted_records, key=lambda row: row[FIELD_START_DATE]) if sort_data else unsorted_records

        for row in records:
            wrtr.writerow(row)
