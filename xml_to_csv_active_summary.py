from typing import Dict, List

import csv
import pathlib

from apple_health_xml_streams import AppleHealthDataActivitySummaryStream
from healthdata import Fieldnames_ActivitySummary, FIELD_DATE
from xml_to_csv_argparser import parse_cmdline


def extract_active_summary(xml_file_path: str) -> List[Dict[str, str]]:
    history: List[Dict[str, str]] = []

    with AppleHealthDataActivitySummaryStream(xml_file_path) as act_sum:
        for elem in act_sum:
            row = elem.attrib.copy()
            history.append(row)

    history.sort(key=lambda x: x[FIELD_DATE])
    return history


def write_csv(csv_filepath: str, active_summary: List[Dict[str, str]]):
    with open(csv_filepath, 'w', encoding='utf-8') as outf:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_ActivitySummary)
        wrtr.writeheader()

        for act_sum in active_summary:
            wrtr.writerow(act_sum)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts Active Summary data from Apple Health Data xml file.")
    active_summary = extract_active_summary(args.xml_filepath)
    write_csv(args.csv_filepath, active_summary)
