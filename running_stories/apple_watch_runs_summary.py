import argparse
import pathlib

import pandas as pd


def apple_watch_run_workouts(data_input_path: str, study_path: str):
    workout = pd.read_csv(f"{data_input_path}/workout.csv",
                          parse_dates=['startDate'], infer_datetime_format=True)

    runs = workout.loc[(workout['workoutActivityType'] == 'HKWorkoutActivityTypeRunning'),
                       ['startDate',  'totalDistance', 'duration', 'HKIndoorWorkout']]

    runs["startDate"] = runs["startDate"].apply(lambda x: x.date())
    runs["HKIndoorWorkout"] = runs['HKIndoorWorkout'].apply(lambda x: True if x == 1.0 else False)

    runs = runs.rename(columns={
        'startDate': 'start_date',
        'totalDistance': 'miles',
        'duration': 'minutes',
        'HKIndoorWorkout': 'indoor_run'
    })

    runs.to_csv(f"{study_path}/apple_watch_runs_summary.csv", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates dataset of runs recorded by apple watch.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date

    data_input_path = f"{home}/small-data/apple-health-csv/full-extract/{partition_date}"
    study_path = f"{home}/small-data/study/running-stories/apple-watch-tracking"
    apple_watch_run_workouts(data_input_path, study_path)
