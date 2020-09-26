import csv
import pathlib
from typing import Any, Dict, Iterator, Tuple

from first_weighin_intervals_mapping import first_weighin_intervals
from utils import Interval


def map_first_weighin_interval_with_activity_date(weighin_intervals: Iterator[Interval],
                                                  activity_metric_summary: Iterator[Dict[str, Any]]) -> Tuple[str, str]:
    try:
        ams = next(activity_metric_summary)
        winterval = next(weighin_intervals)

        while True:
            if winterval.right <= ams['date']:
                winterval = next(weighin_intervals)
            else:
                interval_key = f"<{winterval.left},{winterval.right}>"
                yield interval_key, ams['date']
                while ams := next(activity_metric_summary):
                    if ams['date'] < winterval.right:
                        yield interval_key, ams['date']
                    else:
                        break

    except StopIteration:
        pass


if __name__ == '__main__':
    home = pathlib.Path.home()
    partition_date = "20200925"
    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract"
    weights_csvpath = f"{health_csv_folder}/{partition_date}/bodymass-summary.csv"
    extended_activity_csvpath = f"{health_csv_folder}/{partition_date}/activity_summary_extended.csv"
    interval_activity_dates_csvpath = f"{health_csv_folder}/{partition_date}/activity_dates_first_weighin_intervals.csv"

    with open(weights_csvpath, "r", encoding="utf-8") as f1, \
            open(extended_activity_csvpath, "r", encoding="utf-8") as f2, \
            open(interval_activity_dates_csvpath, "w", encoding="utf-8") as f3:
        wreader = csv.DictReader(f1)
        eareader = csv.DictReader(f2)
        mapwriter = csv.DictWriter(f3, fieldnames=["interval", "date"])
        mapwriter.writeheader()
        weighin_intervals = first_weighin_intervals(wreader)

        for interval, activity_date in map_first_weighin_interval_with_activity_date(weighin_intervals, eareader):
            mapwriter.writerow({"interval": interval, "date": activity_date})
