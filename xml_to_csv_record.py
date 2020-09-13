from typing import Dict, List
import csv

from apple_health_xml_streams import AppleHealthDataRecordTypeStream
from healthdata import *
from utils import localize_apple_health_datetime_str


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

