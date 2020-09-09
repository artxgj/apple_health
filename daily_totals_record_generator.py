from dataclasses import dataclass
from typing import List

import argparse
import csv
import datetime
import pathlib
import sys

from healthkit import HKRecordFactory, HK_APPLE_DATETIME_FORMAT
from myhelpers import DailyAggregator, is_device_iphone, Fieldnames_DailyTotals, DATE_FIELDNAME, UNIT_FIELDNAME, \
    VALUE_FIELDNAME, ymd_path_str


def serialize_summary_csv(csv_source_path: str, csv_dest_path: str, property: str):
    aggregator = DailyAggregator()
    unit = ''

    with open(csv_source_path) as rf:
        rdr = csv.DictReader(rf)

        try:
            row = next(rdr)
            unit = row['unit']
        except StopIteration:
            row = None

        while row is not None:
            hk_record = HKRecordFactory.create(row)
            if not is_device_iphone(hk_record.device):
                start_date = datetime.datetime.strptime(hk_record.start_date, HK_APPLE_DATETIME_FORMAT)
                aggregator.add(start_date, hk_record.value)

            try:
                row = next(rdr)
            except StopIteration:
                row = None

    daily_totals = getattr(aggregator, property)

    with open(csv_dest_path, 'w', encoding='utf-8') as wf:
        wrtr = csv.DictWriter(wf, fieldnames=Fieldnames_DailyTotals)
        wrtr.writeheader()
        keys = sorted(daily_totals.keys())

        for key in keys:
            wrtr.writerow({
                DATE_FIELDNAME: key,
                VALUE_FIELDNAME: daily_totals[key],
                UNIT_FIELDNAME: unit
            })


@dataclass
class AggregatorConfiguration:
    filename: str
    property: str


configs: List[AggregatorConfiguration] = [
    AggregatorConfiguration('distance-walking-running.csv', 'sums'),
    AggregatorConfiguration('resting-heart-rate.csv', 'averages'),
    AggregatorConfiguration('step-count.csv', 'sums'),
    AggregatorConfiguration('body-mass.csv', 'averages'),
    AggregatorConfiguration('exercise-time.csv', 'sums'),
    AggregatorConfiguration('active-energy-burned.csv', 'sums'),
    AggregatorConfiguration('vo2max.csv', 'averages'),
    AggregatorConfiguration('waist-circumference.csv', 'averages'),
]


def gen_month_daily(month_path: str):
    for config in configs:
        csv_source = f'{month_path}/{config.filename}'
        csv_dest = f'{month_path}/daily-totals-{config.filename}'
        serialize_summary_csv(csv_source, csv_dest, config.property)


def gen_lifetime_dailies(etl_path: str):
    for month_path in pathlib.Path(etl_path).iterdir():
        print(f"Generating summaries in {month_path}")
        gen_month_daily(month_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description='generate daily summaries of HK_Record types.')

    parser.add_argument('-y', '--year', type=int, help='year of records to be loaded')
    parser.add_argument('-m', '--month', type=int, help='month of records to be loaded.')
    args = parser.parse_args()

    etl_path = f"{pathlib.Path.home()}/projects-data/apple-health/etl/monthly"

    if args.month is None and args.year is None:
        gen_lifetime_dailies(etl_path)
    elif args.month is None or args.year is None:
        sys.exit()
    elif args.month < 1 or args.month > 12:
        sys.exit(f"{args.month} is not a valid month.")
    else:
        month_path = f"{etl_path}/{ymd_path_str(args.year, args.month)}"
        gen_month_daily(month_path)
