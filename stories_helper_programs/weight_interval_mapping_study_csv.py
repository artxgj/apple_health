import argparse
import csv
import datetime as dt
import itertools
import pathlib
from typing import Any, Dict, Tuple

from intervals import month_firstdate_intervals, map_elements_to_intervals, ElementIntervalPair
from utils import weighin_date_group_key


weight_history_study_fieldnames = ["Date",
                                   "Day",
                                   "Weight",
                                   "Weight Change Since First Day",
                                   "Weight Change Since Last Weigh-in",
                                   "Interval",
                                   "Interval Start Date",
                                   "Interval End Date"]


def weight_history_study_dict(weight_date: str,
                              ordinal_day: int,
                              weight: float,
                              lb_delta_since_first_weighin: float,
                              lb_delta_since_last_weighin: float,
                              ordinal_interval,
                              interval_start_date,
                              interval_end_date) -> Dict[str, Any]:
    return {
            "Date": weight_date,
            "Day": ordinal_day,
            "Weight": round(weight, 3),
            "Weight Change Since First Day": round(lb_delta_since_first_weighin, 3),
            "Weight Change Since Last Weigh-in": round(lb_delta_since_last_weighin, 3),
            "Interval": ordinal_interval,
            "Interval Start Date": interval_start_date,
            "Interval End Date": interval_end_date,
        }


def extract_interval_bounds(pair: ElementIntervalPair) -> Tuple[str, str]:
    if pair is not None:
        interval_start, interval_end = pair.interval.lower_end, pair.interval.upper_end
    else:
        interval_start, interval_end = '', ''

    return interval_start, interval_end


def tocsv_extended_weight_attrs(weights_csvpath: str,
                                weighin_dates_intervals_csvpath: str,
                                start_date: str):
    with open(weights_csvpath, "r", encoding="utf-8") as f1, \
            open(weighin_dates_intervals_csvpath, "w", encoding="utf-8") as f3:

        weighin_reader = csv.DictReader(f1)
        mapwriter = csv.DictWriter(f3, fieldnames=weight_history_study_fieldnames)
        mapwriter.writeheader()
        wrdr1, wrdr2, wrdr3 = itertools.tee(weighin_reader, 3)
        dates_iter = map(lambda x: x['date'], wrdr1)
        intervals = month_firstdate_intervals(dates_iter, weighin_date_group_key, True)
        weighin_dates = map(lambda x: x['date'], wrdr2)

        zipped = itertools.zip_longest(wrdr3, map_elements_to_intervals(weighin_dates, intervals))

        try:
            while unzipped := next(zipped):
                weight, weighin_interval_pair = unzipped
                if weight["date"] >= start_date:
                    break

            interval_start, interval_end = extract_interval_bounds(weighin_interval_pair)
            interval_ordinal: int = 0
            day_ordinal = 0

            first_dt = dt.datetime.strptime(weight["date"], "%Y-%m-%d")
            first_body_mass = float(weight["bodymass"])
            prev_body_mass = first_body_mass
            prev_interval_start = interval_start

            whs = weight_history_study_dict(weight["date"], day_ordinal, first_body_mass, 0, 0,
                                            interval_ordinal, interval_start, interval_end)
            mapwriter.writerow(whs)

            for weight, weighin_interval_pair in zipped:
                interval_start, interval_end = extract_interval_bounds(weighin_interval_pair)

                if interval_start != prev_interval_start:
                    interval_ordinal += 1

                body_mass = float(weight['bodymass'])

                whs = weight_history_study_dict(weight["date"],
                                                (dt.datetime.strptime(weight['date'], "%Y-%m-%d") - first_dt).days,
                                                body_mass,
                                                body_mass - first_body_mass,
                                                body_mass - prev_body_mass,
                                                interval_ordinal, interval_start, interval_end)

                mapwriter.writerow(whs)
                prev_body_mass = body_mass
                prev_interval_start = interval_start

        except StopIteration:
            pass


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
        f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}/weights-intervals-study.csv"

    tocsv_extended_weight_attrs(weights_csvpath, weighin_dates_intervals_csvpath, start_date)
