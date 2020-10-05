import argparse
import csv
import pathlib


def apple_watch_run_workouts(csv_input_file: str, csv_output_file: str):
    with open(csv_input_file, "r", encoding="utf-8") as f1, \
            open(csv_output_file, "w", encoding="utf-8") as f2:
        rdr = csv.DictReader(f1)
        wrtr = csv.DictWriter(f2, fieldnames=["date", "miles", "minutes", "treadmill miles",
                                              "outdoor miles", "year", "year and month"])
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
                    "date": row["startDate"][:10],
                    "miles": miles,
                    "minutes": minutes,
                    "treadmill miles": indoor_miles,
                    "outdoor miles": outdoor_miles,
                    "year": year,
                    "year and month": year_month
                })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates dataset of runs recorded by apple watch.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date

    data_input_path = f"{home}/small-data/apple-health-csv/full-extract/{partition_date}/workout.csv"

    output_path = f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}/" \
                  f"apple-watch-runs-summary-study.csv"
    apple_watch_run_workouts(data_input_path, output_path)
