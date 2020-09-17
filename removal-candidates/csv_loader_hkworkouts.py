import csv
import datetime
import pathlib

from .csv_loader_argparser import parse_cmdline
from utils import date_in_month_predicate, get_apple_health_metadata_entries, localize_apple_health_datetime_str
from cls_apple_health_xml_streams import AppleHealthDataWorkoutStream
from healthkit import HK_APPLE_DATETIME_FORMAT
from healthdata import *


def load_csv(export_xml_path: str,
             output_folder_path: str,
             year: int,
             month: int):
    csv_filepath = f'{output_folder_path}/workouts.csv'

    within_month_range = date_in_month_predicate(year, month)
    with AppleHealthDataWorkoutStream(export_xml_path) as wstream, \
            open(csv_filepath, 'w', encoding='utf-8') as outf:

        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Workout_Csv)
        wrtr.writeheader()

        for elem in wstream:
            start_date = datetime.datetime.strptime(elem.attrib[FIELD_START_DATE], HK_APPLE_DATETIME_FORMAT)
            if within_month_range(start_date):
                replica = elem.attrib.copy()
                replica[FIELD_CREATION_DATE] = localize_apple_health_datetime_str(replica[FIELD_CREATION_DATE])
                replica[FIELD_START_DATE] = localize_apple_health_datetime_str(replica[FIELD_START_DATE])
                replica[FIELD_END_DATE] = localize_apple_health_datetime_str(replica[FIELD_END_DATE])
                meta_row = get_apple_health_metadata_entries(elem, workout_metadata_fields_set)
                wrtr.writerow({**replica, **meta_row})


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description='loads and transforms Workout elements from exported xml file to a csv file.')

    load_csv(export_xml_path=args.export_xml_path,
             output_folder_path=args.csv_folder_path,
             year=args.year,
             month=args.month)
