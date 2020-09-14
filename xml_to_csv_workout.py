from typing import List

import csv
import pathlib

from apple_health_xml_streams import AppleHealthDataWorkoutStream
from healthdata import *
from utils import get_apple_health_metadata_entries, localize_apple_health_datetime_str
from xml_to_csv_argparser import parse_cmdline


def extract_workouts(xml_file_path: str) -> List[Dict[str, str]]:
    history: List[Dict[str, str]] = []

    with AppleHealthDataWorkoutStream(xml_file_path) as wstream:
        for elem in wstream:
            replica = elem.attrib.copy()
            replica[FIELD_CREATION_DATE] = localize_apple_health_datetime_str(replica[FIELD_CREATION_DATE])
            replica[FIELD_START_DATE] = localize_apple_health_datetime_str(replica[FIELD_START_DATE])
            replica[FIELD_END_DATE] = localize_apple_health_datetime_str(replica[FIELD_END_DATE])
            meta_row = get_apple_health_metadata_entries(elem, workout_metadata_fields_set)
            history.append({**replica, **meta_row})

    history.sort(key=lambda x: x[FIELD_START_DATE])
    return history


def write_csv(csv_filepath: str, active_summary: List[Dict[str, str]]):
    with open(csv_filepath, 'w', encoding='utf-8') as outf:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Workout_Csv)
        wrtr.writeheader()

        for act_sum in active_summary:
            wrtr.writerow(act_sum)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts VO2 max history from Apple Health Data xml file.")

    history = extract_workouts(args.xml_filepath)
    write_csv(args.csv_filepath, history)
