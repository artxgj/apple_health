import argparse
import pathlib

import pandas as pd


def ring_closed(x):
    return 1 if x >= 0 else 0


def all_rings_closed(x):
    return 1 if x == 3 else 0


def activity_rings_summary(csv_data_path: str):
    activity_summary = pd.read_csv(f"{csv_data_path}/activity-summary.csv", parse_dates=['dateComponents'])
    activity_rings_data = activity_summary.loc[:, ["dateComponents", "activeEnergyBurned", "appleExerciseTime"]]

    # Apple Health has a row of data with 0 activeEnergyBurned calories on the day before the Apple Watch was activated
    activity_rings_data = activity_rings_data[activity_rings_data["activeEnergyBurned"] > 0]

    activity_rings_data["energy_goal_delta"] = activity_summary["activeEnergyBurned"] - activity_summary[
        "activeEnergyBurnedGoal"]

    activity_rings_data["apple_exercise_time_goal_delta"] = activity_summary["appleExerciseTime"] - activity_summary[
        "appleExerciseTimeGoal"]

    activity_rings_data["apple_stand_hours_goal_delta"] = activity_summary["appleStandHours"] - activity_summary[
        "appleStandHoursGoal"]

    activity_rings_data = activity_rings_data.rename(
        columns={
            'dateComponents': 'date',
            'activeEnergyBurned': 'active_energy_burned',
            'appleExerciseTime': 'apple_exercise_time'
        })

    activity_rings_data["energy_ring_closed"] = activity_rings_data["energy_goal_delta"].map(ring_closed)

    activity_rings_data["exercise_ring_closed"] = activity_rings_data["apple_exercise_time_goal_delta"].map(
        ring_closed)

    activity_rings_data["stand_ring_closed"] = activity_rings_data["apple_stand_hours_goal_delta"].map(ring_closed)

    activity_rings_data["rings_closed"] = activity_rings_data["energy_ring_closed"] + activity_rings_data[
        "exercise_ring_closed"] + activity_rings_data["stand_ring_closed"]

    activity_rings_data["all_rings_closed"] = activity_rings_data["rings_closed"].map(all_rings_closed)
    activity_rings_data.to_csv(f"{csv_data_path}/activity-rings-summary.csv", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date
    csv_data_path = f"{home}/small-data/apple-health-csv/full-extract/{partition_date}"
    activity_rings_summary(csv_data_path)
