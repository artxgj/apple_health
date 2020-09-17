from collections import namedtuple
import argparse
import pathlib


ArgsWorkoutSummary = namedtuple("ArgsWorkoutSummary", ("csv_workout_path", "csv_workout_directory"))


def parse_cmdline(prog: str, description: str) -> ArgsWorkoutSummary:
    parser = argparse.ArgumentParser(prog=prog,
                                     description=description)

    parser.add_argument('-csv-workout-filepath', type=str, required=True, help='path of workout csv file generated by '
                                                                               'etl_csv_workout.py')

    args = parser.parse_args()
    return ArgsWorkoutSummary(args.csv_workout_filepath,
                              pathlib.Path(args.csv_workout_filepath).parent)


