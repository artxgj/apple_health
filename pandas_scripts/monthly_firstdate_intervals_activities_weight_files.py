import argparse
import pathlib

import pandas as pd


# reorganized the generated py file from Jupyter notebook

def month_firstdate_intervals_files(data_input_path: str, study_path: str) -> pd.DataFrame:
    activity_summary_date_interval_map = pd.read_csv(f"{data_input_path}/activity-summary-dates-intervals.csv",
                                                     parse_dates=['date', 'interval_start', 'interval_end'])

    activity_summary_date_interval_map['interval_key'] = \
        activity_summary_date_interval_map['interval_start'].apply(lambda x: x.strftime("%Y%m%d")) + "T" + \
        activity_summary_date_interval_map['interval_end'].apply(lambda x: x.strftime("%Y%m%d"))

    activity_rings_summary = pd.read_csv(f"{data_input_path}/activity-rings-summary.csv", parse_dates=["date"])

    activity_rings_summary_with_intervals = pd.merge(activity_rings_summary,
                                                     activity_summary_date_interval_map,
                                                     left_on='date', right_on='date')

    movement = pd.read_csv(f"{data_input_path}/distance-walking-running-summary.csv", parse_dates=['date'])
    ext_activity_summary = pd.merge(activity_rings_summary_with_intervals, movement[['date', 'movement_distance']],
                                    left_on='date', right_on='date')
    # ### Combine run workout summary
    runs = pd.read_csv(f"{data_input_path}/workout-summary-run.csv", parse_dates=['date'])
    runs = runs.rename(columns={
        'duration': 'run_duration',
        'distance': 'run_distance',
        'energy_burned': 'run_energy_burned'
    })

    ext_activity_summary = pd.merge(ext_activity_summary,
                                    runs[['date', 'run_duration', 'run_distance', 'run_energy_burned']],
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
    ext_activity_summary_groups = ext_activity_summary.groupby('interval_key', as_index=False)

    # ### Create activity-interval averages file

    ext_activity_summary_interval_averages = ext_activity_summary_groups.mean()

    ext_activity_summary_interval_averages = ext_activity_summary_interval_averages.rename(columns={
        "active_energy_burned": "avg_active_energy_burned",
        "apple_exercise_time": "avg_apple_exercise_minutes",
        "energy_goal_delta": "avg_energy_goal_delta",
        "apple_exercise_time_goal_delta": "avg_apple_exercise_time_goal_delta",
        "apple_stand_hours_goal_delta": "avg_apple_stand_hours_goal_delta",
        "energy_ring_closed": "avg_energy_ring_closed",
        "exercise_ring_closed": "avg_exercise_ring_closed",
        "stand_ring_closed": "avg_stand_ring_closed",
        "rings_closed": "avg_rings_closed",
        "all_rings_closed": "avg_all_rings_closed",
        "movement_distance": "avg_movement_miles",
        "run_duration": "avg_run_minutes",
        "run_distance": "avg_run_miles",
        "run_energy_burned": "avg_run_energy_burned",
        "vo2max": "avg_vo2max",
        "resting_heart_rate": "avg_resting_heart_rate"
    })

    ext_activity_summary_interval_averages[[
        "interval_key",
        "avg_active_energy_burned",
        "avg_apple_exercise_minutes",
        "avg_energy_goal_delta",
        "avg_apple_exercise_time_goal_delta",
        "avg_apple_stand_hours_goal_delta",
        "avg_energy_ring_closed",
        "avg_exercise_ring_closed",
        "avg_stand_ring_closed",
        "avg_rings_closed",
        "avg_all_rings_closed",
        "avg_movement_miles",
        "avg_run_minutes",
        "avg_run_miles",
        "avg_run_energy_burned",
        "avg_vo2max",
        "avg_resting_heart_rate"
    ]].to_csv(f"{study_path}/month_firstdate_intervals_activity_averages.csv", index=False)

    # ext_activity_summary_groups.describe()

    ext_activity_summary_groups.describe().to_csv(f"{study_path}/month_firstdate_intervals_activity_statistics.csv",
                                                  index=False, encoding='utf-8')

    # ### Add interval information to ext_activity_summary_interval_averages

    # ### Create Activity Interval Counts

    ext_activity_summary_interval_counts = ext_activity_summary_groups.count()

    ext_activity_summary_interval_counts = ext_activity_summary_interval_counts.rename(columns={
        "date": "activity_interval_days",
        "run_duration": "run_days",
        "vo2max": "vo2max_days",
        "resting_heart_rate": "resting_heart_rate_days"
    })

    ext_activity_summary_interval_counts[["interval_key",
                                          "activity_interval_days",
                                          "run_days",
                                          "vo2max_days",
                                          "resting_heart_rate_days"]].to_csv(
        f"{study_path}/month_firstdate_intervals_activity_counts.csv",
        index=False, encoding='utf-8')

    # ### Create activity interval sums

    ext_activity_interval_sums = ext_activity_summary_groups.sum()

    ext_activity_interval_sums.to_csv(f"{study_path}/month_firstdate_intervals_activity_totals.csv",
                                      index=False, encoding='utf-8')

    # #### drop_duplicates() ~ SELECT DISTINCT

    intervals = pd.merge(ext_activity_summary_interval_averages,
                         activity_summary_date_interval_map[
                             ['interval_key', 'interval_start', 'interval_end']],
                         left_on='interval_key',
                         right_on='interval_key').drop_duplicates()

    return intervals


def weight_interval_file(data_input_path: str,
                         study_path: str,
                         df_intervals: pd.DataFrame):
    # ### Load weight history and create interval weight changes
    weights = pd.read_csv(f"{data_input_path}/bodymass-summary.csv", parse_dates=['date'])

    ### Create starting weight of each interval

    starting_weight = df_intervals.loc[:, ['interval_key', 'interval_start']]

    starting_weight = pd.merge(starting_weight, weights[['date', 'bodymass']], left_on='interval_start',
                               right_on='date')
    ending_weight = df_intervals.loc[:, ['interval_key', 'interval_end']]
    ending_weight = pd.merge(ending_weight, weights[['date', 'bodymass']], left_on='interval_end', right_on='date')
    interval_weight = pd.merge(starting_weight, ending_weight, left_on='interval_key', right_on='interval_key')

    interval_weight = interval_weight.rename(columns={
        'bodymass_x': 'start_weight',
        'bodymass_y': 'end_weight'
    })

    del interval_weight['date_x'], interval_weight['date_y']
    interval_weight['weight_change'] = interval_weight['end_weight'] - interval_weight['start_weight']
    interval_weight['interval_days'] = (interval_weight['interval_end'] - interval_weight['interval_start']).dt.days
    interval_weight['cumul_weight_change'] = interval_weight['weight_change'].cumsum()

    interval_weight[["interval_key",
                     "interval_start",
                     "interval_end",
                     "interval_days",
                     "start_weight",
                     "end_weight",
                     "weight_change",
                     "cumul_weight_change"
                     ]].to_csv(f"{study_path}/month_firstdate_intervals_weights.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-partition-date', type=str, required=True, help='partition-date subfolder')
    args = parser.parse_args()

    home = pathlib.Path.home()
    partition_date = args.partition_date
    data_input_path = f"{home}/small-data/apple-health-csv/full-extract/{partition_date}"
    study_path = f"{home}/small-data/study/health-stories/{partition_date}"
    pathlib.Path(study_path).mkdir(parents=True, exist_ok=True)
    df_intervals = month_firstdate_intervals_files(data_input_path, study_path)
    weight_interval_file(data_input_path, study_path, df_intervals)
