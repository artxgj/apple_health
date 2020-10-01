import argparse
import csv
import itertools
import pathlib

from intervals import month_firstdate_intervals, map_elements_to_intervals
from utils import weighin_date_group_key


def tocsv_weighin_intervals_map(weights_csvpath: str,
                                weighin_dates_intervals_csvpath: str,
                                start_date: str):
    """Map activity summary dates to weigh-in intervals
    This provides a way to calculate total calories, total exercise time, etc. between
    weigh-in periods that are at least a month-apart.
    """
    with open(weights_csvpath, "r", encoding="utf-8") as f1, \
            open(weighin_dates_intervals_csvpath, "w", encoding="utf-8") as f3:

        weighin_reader = csv.DictReader(f1)
        mapwriter = csv.DictWriter(f3, fieldnames=["date", "bodymass", "interval_start", "interval_end", "period"])
        mapwriter.writeheader()
        wrdr1, wrdr2, wrdr3 = itertools.tee(weighin_reader, 3)
        dates_iter = map(lambda x: x['date'], wrdr1)
        intervals = month_firstdate_intervals(dates_iter, weighin_date_group_key, True)
        weighin_dates = map(lambda x: x['date'], wrdr2)

        period = -1
        prev_lower_end = None
        for weight, weighin_map in itertools.zip_longest(wrdr3, map_elements_to_intervals(weighin_dates, intervals)):
            if weight["date"] >= start_date:

                if weighin_map is not None:
                    interval_start, interval_end = weighin_map[1].lower_end, weighin_map[1].upper_end
                else:
                    interval_start, interval_end = '', ''

                if interval_end != prev_lower_end:
                    prev_lower_end = interval_end
                    period += 1

                mapwriter.writerow({
                    "date": weight["date"],
                    "bodymass": weight['bodymass'],
                    "interval_start": interval_start,
                    "interval_end": interval_end,
                    "period": period
                })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    parser.add_argument('-start-date', type=str, required=True, help='desired first weigh-in date')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date
    start_date = args.start_date
    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract"
    weights_csvpath = f"{health_csv_folder}/{partition_date}/bodymass-summary.csv"
    weighin_dates_intervals_csvpath = \
        f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}/first_weighins_intervals.csv"

    tocsv_weighin_intervals_map(weights_csvpath, weighin_dates_intervals_csvpath, start_date)
