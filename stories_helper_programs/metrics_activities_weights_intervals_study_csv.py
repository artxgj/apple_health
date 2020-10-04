import argparse
import pathlib

import pandas as pd


def metrics_activities_weights_intervals_csvs(data_input_path: str, study_path: str):
    activities_weights_intervals = pd.read_csv(f"{study_path}/activities-weights-intervals-study.csv",
                                               parse_dates=['Date', 'Interval Start Date', 'Interval End Date'])

    activity_rings_summary = pd.read_csv(f"{data_input_path}/activity-rings-summary.csv", parse_dates=["date"])

    activity_rings_summary_with_intervals = pd.merge(activity_rings_summary,
                                                     activities_weights_intervals,
                                                     left_on='date', right_on='Date')

    movement = pd.read_csv(f"{data_input_path}/distance-walking-running-summary.csv", parse_dates=['date'])
    ext_activity_summary = pd.merge(activity_rings_summary_with_intervals, movement[['date', 'movement_distance']],
                                    left_on='date', right_on='date')
    # ### Combine run workout summary
    runs = pd.read_csv(f"{data_input_path}/workout-summary-run.csv", parse_dates=['date'])
    runs = runs.rename(columns={
        'duration': 'Run Duration',
        'distance': 'Run Distance',
        'energy_burned': 'Run Energy Burned'
    })

    ext_activity_summary = pd.merge(ext_activity_summary,
                                    runs[['date', 'Run Duration', 'Run Distance', 'Run Energy Burned']],
                                    left_on='date', right_on='date', how='left')

    # ### Combine vo2max summary
    vo2max = pd.read_csv(f"{data_input_path}/vo2max-summary.csv", parse_dates=['date'])

    ext_activity_summary = pd.merge(ext_activity_summary,
                                    vo2max[['date', 'vo2max']],
                                    left_on='date', right_on='date', how='left')

    # ### Combine resting heart rate summary

    resting_heart_rate = pd.read_csv(f"{data_input_path}/resting-heart-rate-summary.csv", parse_dates=['date'])

    ext_activity_summary = pd.merge(ext_activity_summary,
                                    resting_heart_rate[['date', 'resting_heart_rate']],
                                    left_on='date', right_on='date', how='left')

    # ### Create groupby
    ext_activity_summary_groups = ext_activity_summary.groupby('Interval', as_index=False)

    # ### Create activity-interval averages file

    ext_activity_summary_interval_averages = ext_activity_summary_groups.mean()

    ext_activity_summary_interval_averages = ext_activity_summary_interval_averages.rename(columns={
        "active_energy_burned": "Avg. Active Energy Burned",
        "apple_exercise_time": "Avg. Exercise Minutes",
        "energy_goal_delta": "Avg. Move Calories and Move Goal Difference",
        "apple_exercise_time_goal_delta": "Avg. Exercise Time and Exercise Goal Difference",
        "apple_stand_hours_goal_delta": "Avg. Stand Hours and Stand Goal Difference",
        "energy_ring_closed": "Avg. Number of Move Rings Closed",
        "exercise_ring_closed": "Avg. Number of Exercise Rings Closed",
        "stand_ring_closed": "Avg. Number of Stand Rings Closed",
        "rings_closed": "Avg. Number of Rings Closed",
        "all_rings_closed": "Avg. Number of All Rings Closed",
        "movement_distance": "Avg. Distance Moved",
        "Run Duration": "Avg. Run Minutes",
        "Run Distance": "Avg. Run Miles",
        "Run Energy Burned": "Avg. Run Energy Burned",
        "vo2max": "Avg. VO2 Max",
        "resting_heart_rate": "Avg. Resting Heart Rate"
    })

    ext_activity_summary_interval_averages[[
        "Interval",
        "Avg. Active Energy Burned",
        "Avg. Move Calories and Move Goal Difference",
        "Avg. Exercise Minutes",
        "Avg. Exercise Time and Exercise Goal Difference",
        "Avg. Stand Hours and Stand Goal Difference",
        "Avg. Number of Move Rings Closed",
        "Avg. Number of Exercise Rings Closed",
        "Avg. Number of Stand Rings Closed",
        "Avg. Number of Rings Closed",
        "Avg. Number of All Rings Closed",
        "Avg. Distance Moved",
        "Avg. Run Minutes",
        "Avg. Run Miles",
        "Avg. Run Energy Burned",
        "Avg. VO2 Max",
        "Avg. Resting Heart Rate"
    ]].to_csv(f"{study_path}/month-intervals-activity-averages.csv", index=False)

    # ext_activity_summary_groups.describe()

    ext_activity_summary_groups.describe().to_csv(f"{study_path}/month-intervals_activity-statistics.csv",
                                                  index=False, encoding='utf-8')

    # ### Create Activity Interval Counts

    ext_activity_summary_interval_counts = ext_activity_summary_groups.count()

    ext_activity_summary_interval_counts = ext_activity_summary_interval_counts.rename(columns={
        "date": "Number of Days in Interval",
        "Run Duration": "Run Days",
        "vo2max": "VO2 Max Days",
        "resting_heart_rate": "Resting Heart Rate Days"
    })

    ext_activity_summary_interval_counts[["Interval",
                                          "Number of Days in Interval",
                                          "Run Days",
                                          "VO2 Max Days",
                                          "Resting Heart Rate Days"]].to_csv(
        f"{study_path}/month-intervals-activity-counts.csv",
        index=False, encoding='utf-8')

    # ### Create activity interval sums

    ext_activity_interval_sums = ext_activity_summary_groups.sum()

    ext_activity_interval_sums = ext_activity_interval_sums.rename(
        columns={
            "energy_ring_closed": "Move Rings Closed",
            "exercise_ring_closed": "Exercise Rings Closed",
            "stand_ring_closed": "Stand Rings Closed",
            "rings_closed": "Number of Rings Closed",
            "all_rings_closed": "All Rings Closed"
        }
    )

    ext_activity_interval_sums.to_csv(f"{study_path}/month-intervals-activity-totals.csv",
                                      index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date
    data_input_path = f"{home}/small-data/apple-health-csv/full-extract/{partition_date}"
    study_path = f"{home}/small-data/study/apple-watch-health-tracking/{partition_date}"

    pathlib.Path(study_path).mkdir(parents=True, exist_ok=True)

    df_activities_weights_intervals = pd.read_csv(f"{study_path}/activities-weights-intervals-study.csv",
                                                  parse_dates=["Date"])

    metrics_activities_weights_intervals_csvs(data_input_path, study_path)
