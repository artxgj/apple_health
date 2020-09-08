from dateutil import tz
from typing import Callable
import argparse
import csv
import datetime
import pathlib
import sys

from myhelpers import inclusive_month_range, ymd_path_str
from healthkit import HK_APPLE_DATETIME_FORMAT
import healthdata as hd

_metadata_entry_fields = set(hd.Fieldnames_Workout_MetadataEntry)


def load_csvs(export_xml_path: str,
              output_folder_path: str,
              year: int,
              month: int):

    global _metadata_entry_fields
    within_month_range = inclusive_month_range(year, month)

    with open(f'{output_folder_path}/workouts.csv', 'w') as fileobj:
        wrtr = csv.DictWriter(fileobj, fieldnames=hd.Fieldnames_Workout+hd.Fieldnames_Workout_MetadataEntry)
        wrtr.writeheader()

        for elem in hd.get_health_elem(export_xml_path, hd.is_elem_workout):
            if within_month_range(datetime.datetime.strptime(elem.attrib['startDate'], HK_APPLE_DATETIME_FORMAT)):
                row = elem.attrib.copy()
                kv = {mde.attrib['key']: mde.attrib['value'] for mde in elem.findall('MetadataEntry')}

                for k in _metadata_entry_fields:
                    row[k] = kv.get(k, '')

                wrtr.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description='loads selected Record elements from exported xml file to csv files.')

    parser.add_argument('-x', '--xml', type=str, required=True, help='Apple Health exported xml filepath')
    parser.add_argument('-f', '--folder-path', type=str, required=True, help='folder path for output csv files')
    parser.add_argument('-y', '--year', type=int, required=True, help='year of records to be loaded')
    parser.add_argument('-m', '--month', type=int, required=True,
                        help='month of records to be loaded.')

    args = parser.parse_args()

    if args.month < 1 or args.month > 12:
        sys.exit(f"{args.month} is not a valid month.")

    csv_folder_path = pathlib.Path(f"{args.folder_path}/{ymd_path_str(args.year, args.month)}/Workout")

    if not csv_folder_path.exists():
        csv_folder_path.mkdir(parents=True)
    elif not csv_folder_path.is_dir():
        sys.exit(f"{csv_folder_path.absolute()} is not a folder.")

    load_csvs(export_xml_path=args.xml,
              output_folder_path=csv_folder_path.absolute(),
              year=args.year,
              month=args.month)
