import argparse
import csv
import datetime as dt
import pathlib
from collections import namedtuple
from typing import List

from intervals import month_firstdate_intervals, map_elements_to_intervals
from utils import weighin_date_group_key

activity_weight_interval_fieldnames = ["Date", "Day", "Activity",
                                       "Interval", "Interval Start Date", "Interval End Date"]


def activities_weights_intervals_to_dict(activity_date: str, ordinal_day: int, activity: int,
                                         ordinal_interval: int, interval_start_date: str, interval_end_date: str):
    return {
        "Date": activity_date,
        "Day": ordinal_day,
        "Activity": activity,
        "Interval": ordinal_interval,
        "Interval Start Date": interval_start_date,
        "Interval End Date": interval_end_date,
    }


def tocsv_activity_weight_interval_mapping(weights_csvpath: str,
                                           activity_summary_csvpath: str,
                                           activities_weights_intervals_csvpath: str):
    """Map activity summary dates to weigh-in intervals
    This provides a way to calculate total calories, total exercise time, etc. between
    weigh-in periods that are at least a month-apart.
    """
    with open(weights_csvpath, "r", encoding="utf-8") as f1, \
            open(activity_summary_csvpath, "r", encoding="utf-8") as f2, \
            open(activities_weights_intervals_csvpath, "w", encoding="utf-8") as f3:

        weighin_reader = csv.DictReader(f1)
        activity_summary_reader = csv.DictReader(f2)
        mapwriter = csv.DictWriter(f3, fieldnames=activity_weight_interval_fieldnames)
        mapwriter.writeheader()

        dates_iter = map(lambda x: x['date'], weighin_reader)
        weighin_intervals = month_firstdate_intervals(dates_iter, weighin_date_group_key, True)

        activities = filter(lambda x: float(x['activeEnergyBurned']) > 0, activity_summary_reader)
        activities_dates = map(lambda x: x['dateComponents'], activities)
        activity_weighin_interval_mapping = map_elements_to_intervals(activities_dates, weighin_intervals)

        try:
            activity_date, interval = next(activity_weighin_interval_mapping)
            interval_ordinal: int = 0
            activity = 0
            first_dt = dt.datetime.strptime(activity_date, "%Y-%m-%d")
            prev_interval_start = interval.lower_end

            awi = activities_weights_intervals_to_dict(activity_date, 0, activity,
                                                       interval_ordinal, interval.lower_end, interval.upper_end)
            mapwriter.writerow(awi)

            for activity_date, interval in activity_weighin_interval_mapping:
                if interval.lower_end != prev_interval_start:
                    interval_ordinal += 1

                activity += 1

                awi = activities_weights_intervals_to_dict(
                    activity_date,
                    (dt.datetime.strptime(activity_date, "%Y-%m-%d") - first_dt).days,
                    activity,
                    interval_ordinal,
                    interval.lower_end,
                    interval.upper_end)

                mapwriter.writerow(awi)
                prev_interval_start = interval.lower_end

        except StopIteration:
            pass


WeightInterval = namedtuple("WeightInterval", ("weight", "interval", "interval_start_date"))


def start_end_weights_per_activity_interval(weights_csvpath: str,
                                            activities_weights_intervals_csvpath: str) -> List[WeightInterval]:
    with open(weights_csvpath, "r", encoding="utf-8") as f1, \
            open(activities_weights_intervals_csvpath, "r", encoding="utf-8") as f2:
        wrdr = csv.DictReader(f1)
        awi_rdr = csv.DictReader(f2)

        weight_attrs = next(wrdr)
        awi_attrs = next(awi_rdr)
        weight_intervals_index: List[WeightInterval] = []
        next_interval_date = awi_attrs['Interval Start Date']

        try:
            while True:
                if weight_attrs['date'] < next_interval_date:
                    weight_attrs = next(wrdr)
                elif weight_attrs['date'] == next_interval_date:
                    weight_intervals_index.append(WeightInterval(float(weight_attrs['bodymass']),
                                                                 int(awi_attrs['Interval']),
                                                                 awi_attrs['Interval Start Date']))

                    next_interval_date = awi_attrs['Interval End Date']

                    while awi_attrs := next(awi_rdr):
                        if awi_attrs['Interval Start Date'] == next_interval_date:
                            break

        except StopIteration:
            while weight_attrs['date'] < next_interval_date:
                weight_attrs = next(wrdr)

            if len(weight_intervals_index) > 0:
                last = weight_intervals_index[-1]
                if last.interval_start_date < weight_attrs['date']:
                    weight_intervals_index.append(WeightInterval(float(weight_attrs['bodymass']),
                                                                 last[1] + 1,
                                                                 weight_attrs['date']))

    return weight_intervals_index


def tocsv_start_end_weights_per_activity_interval(weight_intervals_index: List[WeightInterval],
                                                  start_end_weights_intervals_csv: str):
    with open(start_end_weights_intervals_csv, "w", encoding="utf-8") as outf:
        wrtr = csv.DictWriter(outf, fieldnames=["Interval", "Number of Days",
                                                "Start Weight", "End Weight",
                                                "Weight Change", "Cumulative Weight Change"])

        wrtr.writeheader()
        iter_start_end_weights_intervals_csv = iter(weight_intervals_index)
        start = next(iter_start_end_weights_intervals_csv)
        cumul_weight_change = 0

        for end in iter_start_end_weights_intervals_csv:
            weight_change = round(end.weight - start.weight, 3)
            cumul_weight_change = round(cumul_weight_change + weight_change, 3)

            size = dt.datetime.strptime(end.interval_start_date, "%Y-%m-%d") - \
                   dt.datetime.strptime(start.interval_start_date, "%Y-%m-%d")

            wrtr.writerow({
                "Interval": start.interval,
                "Number of Days": size.days,
                "Start Weight": start.weight,
                "End Weight": end.weight,
                "Weight Change": weight_change,
                "Cumulative Weight Change": cumul_weight_change
            })
            start = end


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

    study_path = f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}"
    activities_weights_intervals_csvpath = \
        f"{study_path}/activities-weights-intervals-study.csv"

    tocsv_activity_weight_interval_mapping(weights_csvpath,
                                           activity_summary_csvpath,
                                           activities_weights_intervals_csvpath)

    start_end_weights_intervals_csv = f"{study_path}/start-end-weights-activity-intervals.csv"
    weight_intervals_index = start_end_weights_per_activity_interval(weights_csvpath,
                                                                     activities_weights_intervals_csvpath)
    tocsv_start_end_weights_per_activity_interval(weight_intervals_index, start_end_weights_intervals_csv)
