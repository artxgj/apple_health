import argparse
import csv
import pathlib
from typing import List

import intervals


def extract_prime_minutes(workout_run_summary: str,
                          prime_runs_csv_file: str,
                          interval: intervals.Interval):
    prime_number_minutes = {23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

    with open(workout_run_summary, "r", encoding="utf-8") as runf, \
            open(prime_runs_csv_file, "w", encoding="utf-8") as outf:
        rdr = csv.DictReader(runf)
        fieldnames: List[str] = ["Prime Number Minutes"] + rdr.fieldnames
        wrtr = csv.DictWriter(outf, fieldnames=fieldnames)
        wrtr.writeheader()
        for row in rdr:
            if row["date"] in interval:
                minutes = round(float(row["minutes"]))
                if minutes in prime_number_minutes:
                    row["minutes"] = round(float(row["minutes"]), 3)
                    row["miles"] = round(float(row["miles"]), 3)
                    row["Prime Number Minutes"] = minutes
                    wrtr.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates dataset of  runs recorded by apple watch.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date

    study_path = f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}"
    apple_watch_run_summary = f"{study_path}/apple_watch_runs_summary.csv"
    sept2020_prime_runs = f"{study_path}/apple_watch_runs_prime_202009.csv"
    extract_prime_minutes(apple_watch_run_summary,
                          sept2020_prime_runs,
                          intervals.HalfClosedIntervalLeft("2020-09-01", "2020-10-01"))
