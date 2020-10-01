import argparse
import csv
import pathlib

from intervals import month_firstdate_intervals, map_elements_to_intervals
from utils import weighin_date_group_key


def tocsv_activity_interval_map(weights_csvpath: str,
                                activity_summary_csvpath: str,
                                activity_summary_dates_intervals_csvpath: str):
    """Map activity summary dates to weigh-in intervals
    This provides a way to calculate total calories, total exercise time, etc. between
    weigh-in periods that are at least a month-apart.
    """
    with open(weights_csvpath, "r", encoding="utf-8") as f1, \
            open(activity_summary_csvpath, "r", encoding="utf-8") as f2, \
            open(activity_summary_dates_intervals_csvpath, "w", encoding="utf-8") as f3:

        weighin_reader = csv.DictReader(f1)
        actsum_reader = csv.DictReader(f2)
        mapwriter = csv.DictWriter(f3, fieldnames=["date", "interval_start", "interval_end"])
        mapwriter.writeheader()

        dates_iter = map(lambda x: x['date'], weighin_reader)
        intervals = month_firstdate_intervals(dates_iter, weighin_date_group_key, True)

        actsum_dates = map(lambda x: x['dateComponents'], actsum_reader)
        for weighin_date, interval in map_elements_to_intervals(actsum_dates, intervals):
            mapwriter.writerow({
                "date": weighin_date,
                "interval_start": interval.lower_end,
                "interval_end": interval.upper_end
            })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date
    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract"
    weights_csvpath = f"{health_csv_folder}/{partition_date}/bodymass-summary.csv"
    activity_summary_csvpath = f"{health_csv_folder}/{partition_date}/activity-summary.csv"
    activity_summary_dates_intervals_csvpath = \
        f"{health_csv_folder}/{partition_date}/activity-summary-dates-intervals.csv"

    tocsv_activity_interval_map(weights_csvpath,
                                activity_summary_csvpath,
                                activity_summary_dates_intervals_csvpath)
