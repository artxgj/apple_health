import argparse
import csv
import itertools
import pathlib

from typing import Any, Dict, Iterator, Tuple
from utils import groupby_iterators, Interval


def weighin_date_group_key(record: Dict[str, str]) -> str:
    return record['date'][:7]


def monthly_first_last_weighin_dates(weighin_iter: Iterator[Dict[str, Any]]) -> Tuple[str, str]:
    """returns the first and last weigh-in dates of each month
    """
    for key, grouped_iter in groupby_iterators(weighin_iter, weighin_date_group_key):
        grouped_weighins = list(grouped_iter)
        first = grouped_weighins[0]['date']
        last = grouped_weighins[-1]['date']
        yield first, last


def first_weighin_intervals(weighin_iter: Iterator[Dict[str, Any]], include_lastmonth_partial: bool = True) -> \
        Iterator[Interval]:
    first_weighin_iter = monthly_first_last_weighin_dates(weighin_iter)
    left = next(first_weighin_iter)

    for right in first_weighin_iter:
        yield Interval(left[0], right[0])
        left = right

    if include_lastmonth_partial and left[0] < left[1]:
        yield Interval(left[0], left[1])


def map_weighin_date_to_interval(weighins: Iterator[Dict[str, Any]], intervals: Iterator[Interval]):
    try:
        weighin = next(weighins)
        winterval = next(intervals)

        while True:
            if winterval.right <= weighin['date']:
                winterval = next(intervals)
            else:
                yield weighin['date'], winterval.left, winterval.right
                while weighin := next(weighins):
                    if weighin['date'] < winterval.right:
                        yield weighin['date'], winterval.left, winterval.right
                    else:
                        break

    except StopIteration:
        pass


def tocsv_weighins_intervals(weights_csvpath: str,
                             first_weighin_intervals_csvpath: str):

    with open(first_weighin_intervals_csvpath, "w", encoding="utf-8") as wf, \
            open(weights_csvpath, "r", encoding="utf-8") as rf:
            wreader = csv.DictReader(rf)
            mapwriter = csv.DictWriter(wf, fieldnames=["date", "interval_start", "interval_end"])
            mapwriter.writeheader()

            weights_iter1, weights_iter2 = itertools.tee(wreader)
            intervals: Iterator[Interval] = first_weighin_intervals(weights_iter1)

            for weighin_date, interval_start, interval_end in map_weighin_date_to_interval(weights_iter2, intervals):
                mapwriter.writerow({
                    "date": weighin_date,
                    "interval_start": interval_start,
                    "interval_end": interval_end
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
