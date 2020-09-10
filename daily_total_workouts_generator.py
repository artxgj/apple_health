from typing import List, Callable

import argparse
import csv
import datetime
import pathlib
import sys

from healthkit import HKWorkoutWithMetaData, HK_APPLE_DATETIME_FORMAT
from healthdata import Fieldnames_DailyWorkoutsTotals, FIELD_DATE, FIELD_TOTAL_ENERGY_BURNED_UNIT, \
    FIELD_TOTAL_DISTANCE_UNIT, FIELD_DURATION_UNIT, FIELD_TOTAL_ENERGY_BURNED, FIELD_TOTAL_DISTANCE, FIELD_DURATION
from myhelpers import *


def serialize_summary_csv(csv_source_path: str,
                          csv_dest_path: str,
                          device_predicate: Callable[[str], bool]):

    duration_agg = DailyAggregator()
    energy_burned_agg = DailyAggregator()
    distance_agg = DailyAggregator()

    with open(csv_source_path) as rf:
        rdr = csv.DictReader(rf)
        try:
            row = next(rdr)
            duration_unit = row[FIELD_DURATION_UNIT]
            energy_burned_unit = row[FIELD_TOTAL_ENERGY_BURNED_UNIT]
            distance_unit = row[FIELD_TOTAL_DISTANCE_UNIT]

        except StopIteration:
            row = None

        while row is not None:
            workout = HKWorkoutWithMetaData.create(row)
            if device_predicate(workout.device):
                start_date = datetime.datetime.\
                    strptime(workout.start_date, HK_APPLE_DATETIME_FORMAT).\
                    astimezone()

                distance_agg.add(start_date, workout.total_distance)
                energy_burned_agg.add(start_date, workout.total_energy_burned)
                duration_agg.add(start_date, workout.duration)

            try:
                row = next(rdr)
            except StopIteration:
                row = None

    duration_sums = duration_agg.sums
    distance_sums = distance_agg.sums
    energy_burned_sums = energy_burned_agg.sums

    with open(csv_dest_path, 'w', encoding='utf-8') as wf:
        wrtr = csv.DictWriter(wf, fieldnames=Fieldnames_DailyWorkoutsTotals)
        wrtr.writeheader()
        keys = sorted(duration_sums.keys())

        for key in keys:
            wrtr.writerow({
                FIELD_DATE: key,
                FIELD_TOTAL_DISTANCE: distance_sums[key],
                FIELD_TOTAL_DISTANCE_UNIT: distance_unit,
                FIELD_DURATION:duration_sums[key],
                FIELD_DURATION_UNIT: duration_unit,
                FIELD_TOTAL_ENERGY_BURNED: energy_burned_sums[key],
                FIELD_TOTAL_ENERGY_BURNED_UNIT: energy_burned_unit
            })


def gen_month_daily(month_path: str, device_predicate: Callable[[str], bool]):
    csv_source = f'{month_path}/workouts.csv'
    csv_dest = f'{month_path}/daily-totals-workouts.csv'
    serialize_summary_csv(csv_source, csv_dest,  device_predicate)


def gen_lifetime_dailies(etl_path: str, device_predicate: Callable[[str], bool]):
    for month_path in pathlib.Path(etl_path).iterdir():
        print(f"Generating summaries in {month_path}")
        gen_month_daily(str(month_path), device_predicate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description='generate daily summaries of HK_Record types.')

    parser.add_argument('-y', '--year', type=int, help='year of records to be loaded')
    parser.add_argument('-m', '--month', type=int, help='month of records to be loaded.')
    parser.add_argument('-w', '--watch-only', action='store_true',
                        help='process only data generated by or transmitted through Apple Watch')
    args = parser.parse_args()

    etl_path = f"{pathlib.Path.home()}/projects-data/apple-health/etl/monthly"
    device_predicate = watch_only if args.watch_only else always_true

    if args.month is None and args.year is None:
        gen_lifetime_dailies(etl_path, device_predicate)
    elif args.month is None or args.year is None:
        sys.exit(f"month argument is absent." if args.month is None else f"year argument is absent.")
    elif args.month < 1 or args.month > 12:
        sys.exit(f"{args.month} is not a valid month.")
    else:
        month_path = f"{etl_path}/{ymd_path_str(args.year, args.month)}"
        gen_month_daily(month_path, device_predicate)
