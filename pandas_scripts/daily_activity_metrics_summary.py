import argparse
import pathlib
from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class ActivityMetrics:
    date: str  # %Y-%m-%d
    active_energy_burned: float
    apple_exercise_time: float
    weight: Optional[float]
    movement_distance: Optional[float]
    run_duration: Optional[float]
    run_distance: Optional[float]
    run_energy_burned: Optional[float]
    vo2max: Optional[float]
    resting_heart_rate: Optional[float]

    @staticmethod
    def fieldnames() -> List[str]:
        return ["date",
                "active_energy_burned",
                "apple_exercise_time",
                "weight",
                "movement_distance",
                "run_duration",
                "run_distance",
                "run_energy_burned",
                "vo2max",
                "resting_heart_rate"]

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]):
        return cls(
            row["date"],
            float(row["active_energy_burned"]),
            float(row["apple_exercise_time"]),
            None if row["weight"] == '' else float(row["weight"]),
            None if row["movement_distance"] == '' else float(row["movement_distance"]),
            None if row["run_duration"] == '' else float(row["run_duration"]),
            None if row["run_distance"] == '' else float(row["run_distance"]),
            None if row["run_energy_burned"] == '' else float(row["run_energy_burned"]),
            None if row["vo2max"] == '' else float(row["vo2max"]),
            None if row["resting_heart_rate"] == '' else float(row["resting_heart_rate"])
        )


def daily_activity_metrics(data_path: str):
    weights = pd.read_csv(f"{data_path}/bodymass-summary.csv", parse_dates=['date'])
    weights = weights.rename(columns={'bodymass': 'weight'})
    run_workouts = pd.read_csv(f"{data_path}/workout-summary-run.csv", parse_dates=['date'])
    move_distances = pd.read_csv(f"{data_path}/distance-walking-running-summary.csv", parse_dates=['date'])
    vo2max = pd.read_csv(f"{data_path}/vo2max-summary.csv", parse_dates=['date'])
    rest_heart_rate = pd.read_csv(f"{data_path}/resting-heart-rate-summary.csv", parse_dates=['date'])
    activity_summary = pd.read_csv(f"{data_path}/activity-summary.csv", parse_dates=['dateComponents'])
    activity_summary = activity_summary.rename(columns={"dateComponents": "date"})

    daily_combine = pd.merge(
        activity_summary[['date', 'activeEnergyBurned', 'appleExerciseTime']],
        weights[['date', 'weight']],
        left_on='date', right_on='date', how='left')

    daily_combine = pd.merge(daily_combine, move_distances[['date', 'movement_distance']],
                             left_on='date', right_on='date', how='left')

    daily_combine = pd.merge(daily_combine, run_workouts[['date', 'duration', 'distance', 'energy_burned']],
                             left_on='date', right_on='date', how='left')

    daily_combine = pd.merge(daily_combine, vo2max[['date', 'vo2max']], left_on='date', right_on='date', how='left')

    daily_combine = pd.merge(daily_combine, rest_heart_rate[['date', 'resting_heart_rate']],
                             left_on='date', right_on='date', how='left')

    daily_combine = daily_combine.rename(columns={
        'activeEnergyBurned': 'active_energy_burned',
        'appleExerciseTime': 'apple_exercise_time',
        'duration': 'run_duration',
        'distance': 'run_distance',
        'energy_burned': 'run_energy_burned'
    })

    daily_combine.to_csv(f"{data_path}/activity_summary_extended.csv", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="Combine selected dimensions of summaries")

    parser.add_argument('-partition-date',  type=str, required=True)
    args = parser.parse_args()
    home = pathlib.Path.home()
    data_path = f"{home}/small-data/apple-health-csv/full-extract/{args.partition_date}"

    if not pathlib.Path(data_path).exists() or not pathlib.Path(data_path).is_dir():
        raise SystemExit(f"\nProblem with data path {data_path}\n")

    daily_activity_metrics(data_path)
