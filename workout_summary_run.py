import pathlib

from workout_summary_argparser import parse_cmdline
from workout_summary_all import create_workout_summary_file, run_predicate

if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description='Generates workout summary of runs (similar to activity summary).')

    workout_summary_path = f"{args.csv_workout_directory}/workout-summary-run.csv"
    create_workout_summary_file(args.csv_workout_path, workout_summary_path, run_predicate)


