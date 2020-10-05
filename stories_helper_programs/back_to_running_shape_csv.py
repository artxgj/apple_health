import argparse
import csv
import pathlib
from typing import List

from intervals import HalfClosedIntervalLeft
from stories_helper_programs.stories_common import monthly_run_distance_and_duration, MonthlyRunStatistics


def pace(monthly_run_stats: List[MonthlyRunStatistics]) -> List[float]:
    return [round(run.duration/run.distance, 3) for run in monthly_run_stats]


def pace_change_baseline(paces: List[float]) -> List[float]:
    if len(paces) > 1:
        baseline = paces[0]
        return [round(pace-baseline, 3) for pace in paces]
    else:
        return []


def run_shape_stats(runs_filepath: str, run_shape_filepath: str, start_date: str, end_date: str):
    run_stats = monthly_run_distance_and_duration(runs_filepath, HalfClosedIntervalLeft(start_date, end_date))
    run_paces = pace(run_stats)
    pace_changes = pace_change_baseline(run_paces)

    with open(run_shape_filepath, "w", encoding='utf-8') as f1:
        wrtr = csv.DictWriter(f1, fieldnames=[
            "year and month", "duration", "distance", "pace", "pace change from baseline"])
        wrtr.writeheader()

        for run_stat, run_pace, pace_change in zip(run_stats, run_paces, pace_changes):
            wrtr.writerow({
                "year and month": run_stat.name,
                "duration": run_stat.duration,
                "distance": run_stat.distance,
                "pace": run_pace,
                "pace change from baseline": pace_change
            })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates csv of 2020 run stats related to running shape.')

    """
    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    parser.add_argument('-start-date')
    parser.add_argument('-end-date')
    args = parser.parse_args()
    partition_date = args.partition_date
    """
    partition_date = "20201001"
    start_date = "2020-03-17"
    end_date = "2020-10-01"
    home = pathlib.Path.home()
    study_path = f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}"
    runs_filepath = f"{study_path}/apple-watch-runs-summary-study.csv"
    run_shape_filepath = f"{study_path}/running-shape-stats.csv"
    run_shape_stats(runs_filepath, run_shape_filepath, start_date, end_date)
