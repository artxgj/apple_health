from calendar import monthrange

import argparse
import datetime
import pathlib

from etl_csv_all_datasets import generate_datasets
from utils import ymd_path_str

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description="generates by month and year all csv datasets from the exported "
                                                 "Apple Health xml file.")

    parser.add_argument('-xml-filepath',  type=str, required=True, help='Apple Health Data xml file path')
    parser.add_argument('-csv-prefix-path', type=str, required=True, help='csv prefix path tht precedes the year-month'
                                                                          '(format: yyyymm) part. The csv folder will '
                                                                          'be created if it does not exists.')
    parser.add_argument('-year', type=int, required=True, help='year of the month.')
    parser.add_argument('-month', type=int, required=True, help='month')
    parser.add_argument('-watch-only-data', action='store_true', default=False, help='load only watch-generated data')
    parser.add_argument('-sort', action='store_true', default=False, help='sort before saving to csv')

    args = parser.parse_args()
    xml_filepath = pathlib.Path(args.xml_filepath)

    if not xml_filepath.exists() or not xml_filepath.is_file():
        raise SystemExit(f"{xml_filepath} is not a regular file or it does not exist.")

    if args.year < 1970:
        raise SystemExit('The year provided is before 1970.')

    if args.month < 1 or args.month > 12:
        raise SystemExit('The month is not valid.')

    csv_folder = pathlib.Path(f"{args.csv_prefix_path}/{ymd_path_str(args.year, args.month)}")

    if not csv_folder.exists():
        csv_folder.mkdir(parents=True)

    year = args.year
    month = args.month
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, monthrange(year, month)[1], 23, 59, 59)

    generate_datasets(xml_filepath, csv_folder, start_date, end_date, args.sort, args.watch_only_data)
