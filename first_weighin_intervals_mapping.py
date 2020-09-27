import argparse
import csv
import itertools
import pathlib

from intervals import month_firstdate_intervals, map_elements_to_intervals
from utils import weighin_date_group_key


def tocsv_weighins_intervals(weights_csvpath: str,
                             first_weighin_intervals_csvpath: str):

    with open(first_weighin_intervals_csvpath, "w", encoding="utf-8") as wf, \
            open(weights_csvpath, "r", encoding="utf-8") as rf:
            wreader = csv.DictReader(rf)
            mapwriter = csv.DictWriter(wf, fieldnames=["date", "interval_start", "interval_end"])
            mapwriter.writeheader()

            weights_iter1, weights_iter2 = itertools.tee(wreader)
            dates_iter = map(lambda x: x['date'], weights_iter1)
            intervals = month_firstdate_intervals(dates_iter, weighin_date_group_key, True)

            dates_iter = map(lambda x: x['date'], weights_iter2)
            for weighin_date, interval in map_elements_to_intervals(dates_iter, intervals):
                mapwriter.writerow({
                    "date": weighin_date,
                    "interval_start": interval.lower_end,
                    "interval_end": interval.upper_end
                })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="Generate Monthly First Weighin Interval mappings")

    parser.add_argument('-partition-date',  type=str, required=True)
    args = parser.parse_args()
    home = pathlib.Path.home()
    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract/"

    if not pathlib.Path(health_csv_folder).exists() or not pathlib.Path(health_csv_folder).is_dir():
        raise SystemExit(f"\nProblem with data path {health_csv_folder}\n")

    health_csv_folder = f"{home}/small-data/apple-health-csv/full-extract"
    health_csv_partition_folder = f"{health_csv_folder}/{args.partition_date}"
    weights_csvpath = f"{health_csv_partition_folder}/bodymass-summary.csv"
    first_weighin_intervals_csvpath = f"{health_csv_partition_folder}/first_weighin_intervals_map.csv"

    tocsv_weighins_intervals(weights_csvpath, first_weighin_intervals_csvpath)
