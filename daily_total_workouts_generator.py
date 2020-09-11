from typing import Callable

import csv
import datetime
import pathlib

from daily_totals_argparser import parse_cmdline
from healthkit import HKWorkoutWithMetaData, HK_APPLE_DATETIME_FORMAT
from healthdata import Fieldnames_DailyWorkoutsTotals, FIELD_DATE, FIELD_TOTAL_ENERGY_BURNED_UNIT, \
    FIELD_TOTAL_DISTANCE_UNIT, FIELD_DURATION_UNIT, FIELD_TOTAL_ENERGY_BURNED, FIELD_TOTAL_DISTANCE, FIELD_DURATION
from utils import always_true, DailyAggregator, watch_only


def serialize_summary_csv(csv_source_path: str,
                          csv_dest_path: str,
                          device_predicate: Callable[[str], bool],
                          workout_filter: Callable[[str], bool]):

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
            if device_predicate(workout.device) and workout_filter(workout.workout_activity_type):
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


def gen_month_daily(month_path: str,
                    totals_workout_filename: str,
                    device_predicate: Callable[[str], bool],
                    workout_filter: Callable[[str], bool]):
    csv_source = f'{month_path}/workouts.csv'
    csv_dest = f'{month_path}/{totals_workout_filename}.csv'
    serialize_summary_csv(csv_source, csv_dest,  device_predicate, workout_filter)


def gen_lifetime_dailies(etl_path: str,
                         totals_workout_filename: str,
                         device_predicate: Callable[[str], bool],
                         workout_filter: Callable[[str], bool]):
    for month_path in pathlib.Path(etl_path).iterdir():
        print(f"Generating summaries in {month_path}")
        gen_month_daily(str(month_path), totals_workout_filename, device_predicate, workout_filter)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="generates daily summaries of workouts; if year and month are not provided, "
                                     "lifetime daily summaries are generated.")

    device_predicate = always_true if args.include_iphone_data else watch_only

    if args.is_month_daily:
        gen_month_daily(args.folder_path, "daily-totals-workouts", device_predicate, always_true)
    else:
        gen_lifetime_dailies(args.folder_path, "daily-totals-workouts", device_predicate, always_true)
