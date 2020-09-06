from dateutil import tz
from typing import Callable
import argparse
import csv
import datetime
import pathlib
import sys

from myhelpers import inclusive_date_range
from healthkit import HK_APPLE_DATETIME_FORMAT, HK_APPLE_TIMEZONE
import healthdata as hd

_metadata_entry_fields = set(hd.Fieldnames_Workout_MetadataEntry)


def load_csvs(export_xml_path: str,
              output_folder_path: str,
              predicate_date_range: Callable[[datetime.datetime], bool]):

    global _metadata_entry_fields

    with open(f'{output_folder_path}/workouts.csv', 'w') as fileobj:
        wrtr = csv.DictWriter(fileobj, fieldnames=hd.Fieldnames_Workout+hd.Fieldnames_Workout_MetadataEntry)
        wrtr.writeheader()
        for elem in hd.get_health_elem(export_xml_path, hd.is_elem_workout):
            if predicate_date_range(datetime.datetime.strptime(elem.attrib['endDate'], HK_APPLE_DATETIME_FORMAT)):
                row = elem.attrib.copy()
                kj = {mde.attrib['key']: mde.attrib['value'] for mde in elem.findall('MetadataEntry')}

                for k in _metadata_entry_fields:
                    row[k] = kj.get(k, '')

                wrtr.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description='loads selected Record elements from exported xml file to csv files.')

    parser.add_argument('-x', '--xml', type=str, required=True, help='Apple Health exported xml filepath')
    parser.add_argument('-f', '--folder-path', type=str, required=True, help='folder path for output csv files')
    parser.add_argument('-s', '--start-date', type=str,
                        help='extract records that are on or later than this date (YYYY-MM-DD); default is 2015-04-24')
    parser.add_argument('-e', '--end-date', type=str,
                        help='extract records that are on or before this date (YYYY-MM-DD). Default is today.')

    args = parser.parse_args()
    csv_folder_path = pathlib.Path(args.folder_path)

    if not csv_folder_path.exists():
        csv_folder_path.mkdir(parents=True)
    elif not csv_folder_path.is_dir():
        sys.exit(f"{csv_folder_path.absolute()} is not a folder.")

    if args.start_date:
        start_date = datetime.datetime.strptime(f'{args.start_date} {HK_APPLE_TIMEZONE}', '%Y-%m-%d %z')
    else:
        start_date = datetime.datetime.strptime(f'2015-04-24 {HK_APPLE_TIMEZONE}', '%Y-%m-%d %z')

    if args.end_date:
        end_date = datetime.datetime.strptime(f'{args.end_date} {HK_APPLE_TIMEZONE}', '%Y-%m-%d %z')
    else:
        end_date = datetime.datetime.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')} {HK_APPLE_TIMEZONE}",
                                              '%Y-%m-%d %z')

    end_date = end_date.replace(hour=23, minute=59, second=59)

    if end_date < start_date:
        raise ValueError(f'end date is before start date.')

    load_csvs(export_xml_path=args.xml,
              output_folder_path=csv_folder_path.absolute(),
              predicate_date_range=inclusive_date_range(start_date, end_date))

