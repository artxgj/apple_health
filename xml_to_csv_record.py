from typing import Dict, List
import csv

from apple_health_xml_streams import AppleHealthDataRecordTypeStream
from healthdata import FIELD_START_DATE, FIELD_DATE, FIELD_VALUE, FIELD_UNIT, Fieldnames_DailyRecordTotals
from utils import localize_apple_health_datetime_str


def extract_record_type_history(xml_file_path: str, record_type: str) -> List[Dict[str, str]]:
    history: List[Dict[str, str]] = []

    with AppleHealthDataRecordTypeStream(xml_file_path, record_type) as body_mass:
        for elem in body_mass:
            history.append({
                FIELD_DATE: localize_apple_health_datetime_str(elem.attrib[FIELD_START_DATE]),
                FIELD_VALUE: elem.attrib[FIELD_VALUE],
                FIELD_UNIT: elem.attrib[FIELD_UNIT]
            })

    history.sort(key=lambda x: x[FIELD_DATE])
    return history


def write_csv(csv_filepath: str, record_type_history: List[Dict[str, str]]):
    with open(csv_filepath, 'w', encoding='utf-8') as outf:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_DailyRecordTotals)
        wrtr.writeheader()
        wrtr.writerows(record_type_history)

