from collections import namedtuple
import argparse
import pathlib

from utils import ymd_path_str

CsvLoaderArgs = namedtuple("CsvLoaderArgs", ("export_xml_path", "csv_folder_path", "year", "month"))


def parse_cmdline(prog: str, description: str) -> CsvLoaderArgs:
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('-x', '--xml', type=str, required=True, help='Apple Health exported xml filepath')
    parser.add_argument('-f', '--folder-path', type=str, required=True, help='folder path for output csv files')
    parser.add_argument('-y', '--year', type=int, required=True, help='year of records to be loaded')
    parser.add_argument('-m', '--month', type=int, required=True,
                        help='month of records to be loaded.')

    args = parser.parse_args()

    if args.month < 1 or args.month > 12:
        raise ValueError(f"{args.month} is not a valid month.")

    csv_folder_path = pathlib.Path(f"{args.folder_path}/{ymd_path_str(args.year, args.month)}")

    if not csv_folder_path.exists():
        csv_folder_path.mkdir(parents=True)
    elif not csv_folder_path.is_dir():
        raise ValueError(f"{csv_folder_path.absolute()} is not a folder.")

    return CsvLoaderArgs(args.xml, csv_folder_path.absolute(), args.year, args.month)