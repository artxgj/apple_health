import argparse
import datetime
import pathlib
import sys

from myhelpers import date_in_month_predicate, ymd_path_str
from healthkit import HK_APPLE_DATETIME_FORMAT
from hkxmlcsv import HKWorkoutXmlCsvDictWriter, AppleHealthDataReaderContextManager
import healthdata as hd


def load_csvs(export_xml_path: str,
              output_folder_path: str,
              year: int,
              month: int):
    csv_path = f'{output_folder_path}/workouts.csv'

    within_month_range = date_in_month_predicate(year, month)
    with HKWorkoutXmlCsvDictWriter(csv_path, hd.Fieldnames_Workout_Csv) as wrtr, \
            AppleHealthDataReaderContextManager(export_xml_path) as rdr:
        for elem in rdr.read():
            if hd.is_elem_workout(elem):
                start_date = datetime.datetime.strptime(elem.attrib['startDate'], HK_APPLE_DATETIME_FORMAT)
                if within_month_range(start_date):
                    wrtr.write_xml_elem(elem)


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

    csv_folder_path = pathlib.Path(f"{args.folder_path}/{ymd_path_str(args.year, args.month)}")

    if not csv_folder_path.exists():
        csv_folder_path.mkdir(parents=True)
    elif not csv_folder_path.is_dir():
        sys.exit(f"{csv_folder_path.absolute()} is not a folder.")

    load_csvs(export_xml_path=args.xml,
              output_folder_path=csv_folder_path.absolute(),
              year=args.year,
              month=args.month)
