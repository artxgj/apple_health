from datetime import datetime
from typing import Dict, List

import csv
import pathlib

from apple_health_xml_streams import AppleHealthDataActivitySummaryStream

from healthdata import Fieldnames_ActivitySummary, FIELD_DATE
from healthkit import HK_APPLE_DATE_FORMAT
from utils import element_to_dict, between_dates_predicate

from xml_to_csv_argparser import parse_cmdline


def xml_to_csv(xml_file_path: str,
               csv_filepath: str,
               start_date: datetime,
               end_date: datetime,
               *arg):

    with open(csv_filepath, 'w', encoding='utf-8') as outf, \
            AppleHealthDataActivitySummaryStream(xml_file_path) as wstream:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_ActivitySummary)
        wrtr.writeheader()

        in_date_boundary = between_dates_predicate(start_date, end_date)

        active_summary_dict = map(element_to_dict, wstream)

        dates_bounded_active_summaries = filter(lambda row: in_date_boundary(
            datetime.strptime(row[FIELD_DATE], HK_APPLE_DATE_FORMAT)), active_summary_dict)

        for row in dates_bounded_active_summaries:
            wrtr.writerow(row)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts Active Summary data from Apple Health Data xml file.")

    xml_to_csv(args.xml_filepath, args.csv_filepath,
               args.start_date, args.end_date,
               args.sort, args.watch_only_data)

