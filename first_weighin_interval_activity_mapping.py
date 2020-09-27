import csv
import pathlib
from typing import Any, Dict, Iterator, Tuple

from intervals import month_firstdate_intervals, map_elements_to_intervals
from utils import weighin_date_group_key


def tocsv_activity_interval_map(weights_csvpath: str,
                                activity_summary_csvpath: str,
                                activity_summary_dates_intervals_csvpath: str):
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
    home = pathlib.Path.home()
    partition_date = "20200925"
    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract"
    weights_csvpath = f"{health_csv_folder}/{partition_date}/bodymass-summary.csv"
    activity_summary_csvpath = f"{health_csv_folder}/{partition_date}/activity-summary.csv"
    activity_summary_dates_intervals_csvpath = \
        f"{health_csv_folder}/{partition_date}/activity-summary-dates-intervals.csv"

    tocsv_activity_interval_map(weights_csvpath,
                                activity_summary_csvpath,
                                activity_summary_dates_intervals_csvpath)
