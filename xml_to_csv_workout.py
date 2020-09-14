from typing import Dict, List

import csv
import pathlib

from apple_health_xml_streams import AppleHealthDataWorkoutStream
from healthdata import FIELD_START_DATE, Fieldnames_Workout_Csv, Fieldnames_Workout_MetadataEntry
from utils import get_apple_health_metadata_entries
from xml_to_csv_argparser import parse_cmdline


_metadata_entry_fields = set(Fieldnames_Workout_MetadataEntry)


def extract_workouts(xml_file_path: str) -> List[Dict[str, str]]:
    history: List[Dict[str, str]] = []

    with AppleHealthDataWorkoutStream(xml_file_path) as wstream:
        for elem in wstream:
            row = elem.attrib.copy()
            meta_row = get_apple_health_metadata_entries(elem, _metadata_entry_fields)
            history.append({**row, **meta_row})

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
