from dataclasses import dataclass
from typing import List, Callable

import csv
import datetime
import pathlib

from daily_totals_argparser import parse_cmdline
from healthkit import HKRecordFactory, HK_APPLE_DATETIME_FORMAT
from healthdata import Fieldnames_DailyRecordTotals, FIELD_DATE, FIELD_UNIT, FIELD_VALUE
from utils import *


def serialize_summary_csv(csv_source_path: str,
                          csv_dest_path: str,
                          property: str,
                          device_predicate: Callable[[str], bool]):

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
            if device_predicate(hk_record.device):
                start_date = datetime.datetime.strptime(hk_record.start_date, HK_APPLE_DATETIME_FORMAT)

                # calling astimezone() matches the local display of ios Health app records
                aggregator.add(start_date.astimezone(), hk_record.value)

            try:
                row = next(rdr)
            except StopIteration:
                row = None

    daily_totals = getattr(aggregator, property)

    with open(csv_dest_path, 'w', encoding='utf-8') as wf:
        wrtr = csv.DictWriter(wf, fieldnames=Fieldnames_DailyRecordTotals)
        wrtr.writeheader()
        keys = sorted(daily_totals.keys())

        for key in keys:
            wrtr.writerow({
                FIELD_DATE: key,
                FIELD_VALUE: daily_totals[key],
                FIELD_UNIT: unit
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


def gen_month_daily(month_path: str, device_predicate: Callable[[str], bool]):
    for config in configs:
        csv_source = f'{month_path}/{config.filename}'
        csv_dest = f'{month_path}/daily-totals-{config.filename}'
        serialize_summary_csv(csv_source, csv_dest, config.property, device_predicate)


def gen_lifetime_dailies(etl_path: str, device_predicate: Callable[[str], bool]):
    for month_path in pathlib.Path(etl_path).iterdir():
        print(f"Generating summaries in {month_path}")
        gen_month_daily(str(month_path), device_predicate)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="generates daily summaries of HK_Record types; if year and month are not provided,"
                                     " lifetime daily summaries are generated.")

    device_predicate = always_true if args.include_iphone_data else watch_only

    if args.is_month_daily:
        gen_month_daily(args.folder_path, device_predicate)
    else:
        gen_lifetime_dailies(args.folder_path, device_predicate)
