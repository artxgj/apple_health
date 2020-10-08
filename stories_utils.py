import functools
import itertools
import statistics
from collections import namedtuple
from typing import Any, Callable, Dict, Iterator, List, Sequence, Tuple, Union

from intervals import Interval
from utils import csvdict_generator, always_true

MonthlyRunStatistics = namedtuple("RunDurationAndDistance", ("name", "duration", "distance"))
IntervalMeanCount = namedtuple("IntervalMeanCount", ("name", "mean", "count"))
IntervalPace = namedtuple("IntervalPace", ("name", "pace", "duration", "distance", "count"))


def daterange_filter(date_key: str, interval: Interval):
    def fn(x) -> bool:
        return x[date_key] in interval
    return fn


def add(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    return x + y


def translate_sequence(seq: Sequence[Union[int, float]], offset: Union[int, float]) -> List[Union[int, float]]:
    return [elem + offset for elem in seq]


def pace(duration: float, distance: float):
    return round(duration/distance, 2)


def intervals_attributes(filepath: str,
                         interval_keyfunc: Callable[[Any], str],
                         date_filter_fn: Callable[[str], bool] = always_true) -> \
        Iterator[Tuple[Any, Iterator[Dict[str, Any]]]]:
    return itertools.groupby(filter(date_filter_fn, csvdict_generator(filepath)), interval_keyfunc)


def intervals_mean(intervals_attrs: Iterator[Tuple[Any, Iterator[Dict[str, Any]]]], column_name: str) -> \
        List[IntervalMeanCount]:
    intervals_mean_count: List[IntervalMeanCount] = []

    for interval_name, iter_interval_attrs in intervals_attrs:
        interval_attrs = tuple(iter_interval_attrs)
        intervals_mean_count.append(IntervalMeanCount(
            interval_name,
            round(statistics.mean([float(c[column_name]) for c in interval_attrs]), 2),
            len(interval_attrs)))

    return intervals_mean_count


def intervals_workout_pace(workout_attrs: Iterator[Tuple[Any, Iterator[Dict[str, Any]]]]) -> List[IntervalPace]:
    intervals_pace_count: List[IntervalPace] = []

    for key, workout_iter in workout_attrs:
        interval_workouts = tuple(workout_iter)
        total_duration = round(functools.reduce(add, [float(w['duration']) for w in interval_workouts]), 2)
        total_distance = round(functools.reduce(add, [float(w['distance']) for w in interval_workouts]), 2)
        interval_pace = pace(total_duration, total_distance)
        intervals_pace_count.append(IntervalPace(key, round(interval_pace, 2),
                                                 total_duration, total_distance,
                                                 len(interval_workouts)))

    return intervals_pace_count


def monthly_run_distance_and_duration(runs_filepath: str, interval: Interval) -> List[MonthlyRunStatistics]:
    in_date_range = daterange_filter(interval)

    run_stats: List[MonthlyRunStatistics] = []
    grouped_runs = itertools.groupby(filter(in_date_range, csvdict_generator(runs_filepath)),
                                     lambda x: x['date'][:7])

    for key, runs in grouped_runs:
        month_runs = list(runs)
        minutes = functools.reduce(add, [float(run['minutes']) for run in month_runs])
        miles = functools.reduce(add, [float(run['miles']) for run in month_runs])
        run_stats.append(MonthlyRunStatistics(key, round(minutes, 3), round(miles, 3)))

    return run_stats
