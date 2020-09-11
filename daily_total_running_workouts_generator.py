import pathlib

from daily_totals_argparser import parse_cmdline
from daily_total_workouts_generator import gen_month_daily, gen_lifetime_dailies
from healthdata import WORKOUT_RUN
from utils import always_true, watch_only


def is_running_workout(workout: str):
    return workout == WORKOUT_RUN


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="generates daily summaries of running workouts; "
                                     "if year and month are not provided, lifetime daily summaries are generated.")

    device_predicate = always_true if args.include_iphone_data else watch_only

    if args.is_month_daily:
        gen_month_daily(args.folder_path, "daily-totals-running-workouts", device_predicate, is_running_workout)
    else:
        gen_lifetime_dailies(args.folder_path, "daily-totals-running-workouts", device_predicate, is_running_workout)
