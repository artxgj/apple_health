from typing import Any, Optional

import csv
import pathlib

from monthly_totals_argparser import parse_cmdline
from healthdata import *


_workouts_config = [
    (WORKOUT, 'daily-totals-workouts.csv'),
    (WORKOUT_RUN, 'daily-totals-running-workouts.csv'),
    (WORKOUT_WALK, 'daily-totals-walking-workouts.csv')
]


def sum_month_values(csv_file_path: str) -> Optional[Dict[str, Any]]:
    with open(csv_file_path, 'r') as input_file:
        rdr = csv.DictReader(input_file)
        try:
            row = next(rdr)
        except StopIteration:
            return None

        entries = 1
        month_sums = {
            FIELD_DATE: row[FIELD_DATE][:7],
            FIELD_DURATION: float(row[FIELD_DURATION]),
            FIELD_DURATION_UNIT: row[FIELD_DURATION_UNIT],
            FIELD_TOTAL_DISTANCE: float(row[FIELD_TOTAL_DISTANCE]),
            FIELD_TOTAL_DISTANCE_UNIT: row[FIELD_TOTAL_DISTANCE_UNIT],
            FIELD_TOTAL_ENERGY_BURNED: float(row[FIELD_TOTAL_ENERGY_BURNED]),
            FIELD_TOTAL_ENERGY_BURNED_UNIT: row[FIELD_TOTAL_ENERGY_BURNED_UNIT],
            'days': 1
        }

        for row in rdr:
            entries += 1
            month_sums[FIELD_TOTAL_DISTANCE] += float(row[FIELD_TOTAL_DISTANCE])
            month_sums[FIELD_TOTAL_ENERGY_BURNED] += float(row[FIELD_TOTAL_ENERGY_BURNED])
            month_sums[FIELD_DURATION] += float(row[FIELD_DURATION])
            month_sums['days'] += 1

        return month_sums


def gen_month_summary(etl_month_path: pathlib.Path):
    with open(f'{str(etl_month_path)}/monthly-totals-workouts.csv', 'w', encoding='utf-8') as fo:
        wrtr = csv.DictWriter(fo, fieldnames=Fieldnames_MonthlyWorkoutsTotals)
        wrtr.writeheader()

        for wc in _workouts_config:
            x = pathlib.Path(f'{etl_month_path}/{wc[1]}')
            summary = sum_month_values(str(x))

            if summary is not None:
                summary[FIELD_WORKOUT_ACTIVITY] = wc[0]
                wrtr.writerow(summary)


def gen_lifetime_month_summaries(etl_path: str):
    for month_path in pathlib.Path(etl_path).iterdir():
        print(f"Generating monthly workout summary in {month_path}")
        gen_month_summary(month_path)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="generates monthly summaries of workouts; if year and month are not provided, "
                                     "lifetime monthly summaries are generated.")

    if args.is_monthly:
        gen_month_summary(args.etl_path)
    else:
        gen_lifetime_month_summaries(args.etl_path)

