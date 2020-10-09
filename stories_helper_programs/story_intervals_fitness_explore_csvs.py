import argparse
import csv
from collections import namedtuple
from typing import Any, Callable, Dict, List, Union

from intervals import HalfClosedIntervalLeft
from stories_utils import (
    daterange_filter, translate_sequence,
    intervals_attributes,
    intervals_mean, intervals_workout_pace,
    IntervalMeanCount, IntervalPace)


_DEFAULT_TRANSLATION_OFFSET = 15

DimensionConfig = namedtuple("DimensionConfig",
                             ("source_filename", "column_name",
                              "output_name", "translate_too", "translate_offset"))


_dimension_csv_configs = [
    DimensionConfig("bodymass-summary.csv", "bodymass",
                    "fitness-average-weight", True, _DEFAULT_TRANSLATION_OFFSET),

    DimensionConfig("distance-walking-running-summary.csv", "movement_distance",
                    "fitness-average-movement-distance", False, 0),

    DimensionConfig("workout-summary-run.csv", "distance",
                    "fitness-average-run-distance", False, 0),

    DimensionConfig("resting-heart-rate-summary.csv", "resting_heart_rate",
                    "fitness-average-restheart", True, _DEFAULT_TRANSLATION_OFFSET),

    DimensionConfig("vo2max-summary.csv", "vo2max",
                    "fitness-average-vo2max", True, 7)
]


def dimension_month_interval_date(dimension: Dict[str, Any]) -> str:
    # returns %Y-%m substring of date string
    return dimension['date'][:7]


def intervals_translated_csv(csvfilepath: str,
                             interval_mean_counts: List[IntervalMeanCount],
                             offset: Union[int, float] = 0):
    mean_vector = [e.mean for e in interval_mean_counts]
    translated_mean_vector = translate_sequence(mean_vector, -mean_vector[0] + offset)

    with open(csvfilepath, "w", encoding="utf-8") as tf:
        wrtr = csv.DictWriter(tf, fieldnames=["Interval", "Days", "Translated Mean"])
        wrtr.writeheader()

        for imc, tm in zip(interval_mean_counts, translated_mean_vector):
            wrtr.writerow({
                "Interval": imc.name,
                "Days": imc.count,
                "Translated Mean": tm
            })


def month_intervals_means(dimension_filepath: str,
                          column_name: str,
                          date_range_filter: Callable[[str], bool]) -> List:
    monthly_interval_dimension = intervals_attributes(
        f"{dimension_filepath}", dimension_month_interval_date, date_range_filter)

    return intervals_mean(monthly_interval_dimension, column_name)


def to_csv_dimension_mean(csvfilepath: str, dimension_mean: List[IntervalMeanCount]):
    with open(csvfilepath, "w", encoding="utf-8") as df:
        wrtr = csv.DictWriter(df, fieldnames=["Interval", "Days", "Mean"])
        wrtr.writeheader()

        for imc in dimension_mean:
            wrtr.writerow({
                "Interval": imc.name,
                "Days": imc.count,
                "Mean": imc.mean
            })


def month_intervals_means_csvs(source_data_path: str,
                               story_data_path: str,
                               story_daterange_filter: Callable[[str], bool]):

    for dcc in _dimension_csv_configs:
        dimension_mean = month_intervals_means(f"{source_data_path}/{dcc.source_filename}",
                                               dcc.column_name, story_daterange_filter)

        to_csv_dimension_mean(f"{story_data_path}/{dcc.output_name}.csv", dimension_mean)

        if dcc.translate_too:
            intervals_translated_csv(f"{story_data_path}/{dcc.output_name}-translated.csv",
                                     dimension_mean, dcc.translate_offset)


def month_intervals_pace(workout_filepath: str,
                         date_range_filter: Callable[[str], bool],
                         interval_keyfunc: Callable[[Dict[str, Any]], str]) -> List[IntervalPace]:
    intervals_workouts = intervals_attributes(
        f"{workout_filepath}", interval_keyfunc, date_range_filter)

    return intervals_workout_pace(intervals_workouts)


def month_intervals_pace_csv(workout_filepath: str, story_data_path: str,
                             story_daterange_filter: Callable[[str], bool]):
    month_workouts: List[IntervalPace] = month_intervals_pace(workout_filepath, story_daterange_filter,
                                                              dimension_month_interval_date)
    pace_vector = [w.pace for w in month_workouts]
    zero_translated_pace = translate_sequence(pace_vector, -pace_vector[0])
    month_pace_csv = f"{story_data_path}/fitness-month-pace.csv"

    with open(month_pace_csv, "w", encoding="utf-8") as fo1:
        wrtr = csv.DictWriter(fo1, fieldnames=["Interval", "Days", "Pace", "Translated Pace", "Duration", "Distance"])
        wrtr.writeheader()

        for workout, translated_pace in zip(month_workouts, zero_translated_pace):
            wrtr.writerow({
                "Interval": workout.name,
                "Days": workout.count,
                "Pace": workout.pace,
                "Translated Pace": round(translated_pace, 2),
                "Duration": workout.duration,
                "Distance": workout.distance
            })

    intervals_pace_mean = [IntervalMeanCount(w.name, w.pace, w.count) for w in month_workouts]
    intervals_translated_csv(f"{story_data_path}/fitness-average-pace-translated.csv", intervals_pace_mean,
                             _DEFAULT_TRANSLATION_OFFSET)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates csv files for dimension-averages exploration story')
    parser.add_argument('-input-datapath', type=str, required=True)
    parser.add_argument('-story-datapath', type=str, required=True,)
    parser.add_argument('-partition-date', type=str, required=True, help="partition-date (%Y%m%d) name of subfolder")
    parser.add_argument('-start-date', type=str, required=True,  help="%Y-%m-%d")
    parser.add_argument('-end-date', type=str, required=True,  help="%Y-%m-%d")

    args = parser.parse_args()
    story_data_path = f"{args.story_datapath}/{args.partition_date}"
    source_data_path = f"{args.input_datapath}/{args.partition_date}"

    in_story_daterange = daterange_filter("date", HalfClosedIntervalLeft(args.start_date, args.end_date))
    month_intervals_means_csvs(source_data_path, story_data_path, in_story_daterange)
    month_intervals_pace_csv(f"{source_data_path}/workout-summary-run.csv", story_data_path, in_story_daterange)

