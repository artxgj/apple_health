from collections import namedtuple
import argparse
import pathlib

from utils import ymd_path_str

DailyTotalsArgs = namedtuple("DailyTotalsArgs", ("folder_path", "include_iphone_data", "is_month_daily"))


def parse_cmdline(prog: str, description: str) -> DailyTotalsArgs:
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('-y', '--year', type=int, help='year of records to be loaded')
    parser.add_argument('-m', '--month', type=int, help='month of records to be loaded.')
    parser.add_argument('-i', '--include-iphone-data', action='store_true',
                        help='include iphone-generated data.')
    args = parser.parse_args()

    etl_path = f"{pathlib.Path.home()}/projects-data/apple-health/etl/monthly"

    if args.month is None and args.year is None:
        return DailyTotalsArgs(etl_path, args.include_iphone_data, False)
    elif args.month is None or args.year is None:
        message = "month argument is absent." if args.month is None else "year argument is absent."
        raise ValueError(message)
    elif args.month < 1 or args.month > 12:
        raise ValueError(f"{args.month} is not a valid month.")
    else:
        month_path = f"{etl_path}/{ymd_path_str(args.year, args.month)}"
        return DailyTotalsArgs(month_path, args.include_iphone_data, True)
