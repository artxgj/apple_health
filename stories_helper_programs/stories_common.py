import functools
import itertools
from collections import namedtuple
from typing import List, Union

from intervals import Interval
from utils import csvdict_generator

MonthlyRunStatistics = namedtuple("RunDurationAndDistance", ("name", "duration", "distance"))


def date_filter(interval: Interval):
    def fn(x) -> bool:
        return x['date'] in interval
    return fn


def add(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    return x + y


def monthly_run_distance_and_duration(runs_filepath: str, interval: Interval) -> List[MonthlyRunStatistics]:
    in_date_range = date_filter(interval)

    run_stats: List[MonthlyRunStatistics] = []
    grouped_runs = itertools.groupby(filter(in_date_range, csvdict_generator(runs_filepath)),
                                     lambda x: x['date'][:7])

    for key, runs in grouped_runs:
        month_runs = list(runs)
        minutes = functools.reduce(add, [float(run['minutes']) for run in month_runs])
        miles = functools.reduce(add, [float(run['miles']) for run in month_runs])
        run_stats.append(MonthlyRunStatistics(key, round(minutes, 3), round(miles, 3)))

    return run_stats
