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
        mapwriter = csv.DictWriter(f3, fieldnames=["date", "interval_start", "interval_end"])
        mapwriter.writeheader()
        wr1, wr2 = itertools.tee(weighin_reader)
        dates_iter = map(lambda x: x['date'], wr1)
        intervals = month_firstdate_intervals(dates_iter, weighin_date_group_key, True)
        weighin_dates = map(lambda x: x['date'], wr2)

        for weighin_date, interval in map_elements_to_intervals(weighin_dates, intervals):
            if weighin_date >= start_date:
                mapwriter.writerow({
                    "date": weighin_date,
                    "interval_start": interval.lower_end,
                    "interval_end": interval.upper_end
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
        f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}/first-weighins-intervals.csv"

    tocsv_weighin_intervals_map(weights_csvpath, weighin_dates_intervals_csvpath, start_date)
