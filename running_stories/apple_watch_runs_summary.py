import argparse
import csv
import pathlib

import pandas as pd

"""
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
"""


def apple_watch_run_workouts(csv_input_file: str, csv_output_file: str):
    with open(csv_input_file, "r", encoding="utf-8") as f1, \
            open(csv_output_file, "w", encoding="utf-8") as f2:
        rdr = csv.DictReader(f1)
        wrtr = csv.DictWriter(f2, fieldnames=["start_date", "miles", "minutes", "indoor_miles",
                                              "outdoor_miles", "year", "year_month"])
        wrtr.writeheader()

        for row in rdr:
            if row['workoutActivityType'] == "HKWorkoutActivityTypeRunning":
                year = row['startDate'][:4]
                miles: str = str(round(float(row['totalDistance']), 3))
                if row['HKIndoorWorkout'] == '1':
                    indoor_miles = miles
                    outdoor_miles = ''
                else:
                    indoor_miles = ''
                    outdoor_miles = miles

                minutes: str = str(round(float(row['duration']), 3))
                year_month = row["startDate"][:7]
                wrtr.writerow({
                    "start_date": row["startDate"][:10],
                    "miles": miles,
                    "minutes": minutes,
                    "indoor_miles": indoor_miles,
                    "outdoor_miles": outdoor_miles,
                    "year": year,
                    "year_month": year_month
                })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates dataset of runs recorded by apple watch.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date

    data_input_path = f"{home}/small-data/apple-health-csv/full-extract/{partition_date}/workout.csv"

    output_path = f"{home}/small-data/study/running-stories/apple-watch-tracking/apple_watch_runs_summary.csv"
    apple_watch_run_workouts(data_input_path, output_path)
