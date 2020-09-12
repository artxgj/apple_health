from typing import Any, Optional

import csv
import pathlib

from monthly_totals_argparser import parse_cmdline
from healthdata import *


_workouts_config = [
    (HK_REC_TYPE_DistanceWalkingRunning, 'daily-totals-distance-walking-running.csv'),
    (HK_REC_TYPE_RestingHeartRate, 'daily-totals-resting-heart-rate.csv'),
    (HK_REC_TYPE_StepCount, 'daily-totals-step-count.csv'),
    (HK_REC_TYPE_BodyMass, 'daily-totals-body-mass.csv'),
    (HK_REC_TYPE_AppleExerciseTime, 'daily-totals-exercise-time.csv'),
    (HK_REC_TYPE_ActiveEnergyBurned, 'daily-totals-active-energy-burned.csv'),
    (HK_REC_TYPE_VO2Max, 'daily-totals-vo2max.csv'),
    (HK_REC_TYPE_WaistCircumference, 'daily-totals-waist-circumference.csv'),
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
            FIELD_VALUE: float(row[FIELD_VALUE]),
            FIELD_UNIT: row[FIELD_UNIT],
            'days': 1
        }

        for row in rdr:
            entries += 1
            month_sums[FIELD_VALUE] += float(row[FIELD_VALUE])
            month_sums['days'] += 1

        return month_sums


def gen_month_summary(etl_month_path: pathlib.Path):
    with open(f'{str(etl_month_path)}/monthly-totals-hk-records.csv', 'w', encoding='utf-8') as fo:
        wrtr = csv.DictWriter(fo, fieldnames=Fieldnames_MonthlyRecordTotals)
        wrtr.writeheader()

        for wc in _workouts_config:
            x = pathlib.Path(f'{etl_month_path}/{wc[1]}')
            summary = sum_month_values(str(x))

            if summary is not None:
                summary[FIELD_TYPE] = wc[0]
                wrtr.writerow(summary)


def gen_lifetime_month_summaries(etl_path: str):
    for month_path in pathlib.Path(etl_path).iterdir():
        print(f"Generating monthly records summary in {month_path}")
        gen_month_summary(month_path)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="generates monthly summaries of HK_Record types; if year and month are not "
                                     "provided, lifetime monthly summaries are generated.")

    if args.is_monthly:
        gen_month_summary(args.etl_path)
    else:
        gen_lifetime_month_summaries(args.etl_path)
