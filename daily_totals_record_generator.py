import csv
import datetime

from healthkit import HKRecordFactory, HK_APPLE_DATETIME_FORMAT
from myhelpers import DailyAggregator, is_device_iphone, Fieldnames_DailyTotals, DATE_FIELDNAME, UNIT_FIELDNAME, VALUE_FIELDNAME


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


