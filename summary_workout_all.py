from typing import Callable
import csv
import pathlib

from cls_healthkit import HKWorkout
from constants_apple_health_data import WORKOUT_RUN, WORKOUT_WALK, csv_fieldnames_workout_summary
from cls_sample_summary import WorkoutSummary, WorkoutSummaryRecord
from utils import always_true
from summary_workout_argparser import parse_cmdline


def run_predicate(workout_type: str):
    return workout_type == WORKOUT_RUN


def walk_predicate(workout_type: str):
    return workout_type == WORKOUT_WALK


def create_workout_summary_file(workout_csv_filepath: str,
                                workout_summary_filepath: str,
                                include_workout: Callable[[str], bool]):
    with open(workout_csv_filepath, "r", encoding='utf-8') as rf:
        reader = csv.DictReader(rf)
        summary = None
        try:
            record = HKWorkout.create(next(reader))

            summary = WorkoutSummary(record.duration_unit,
                                     record.total_distance_unit,
                                     record.total_energy_burned_unit)

            if include_workout(record.workout_activity_type):
                summary.tally(record)

            for row in reader:
                record = HKWorkout.create(row)
                if include_workout(record.workout_activity_type):
                    summary.tally(record)

        except StopIteration:
            pass

    if summary is not None:
        with open(workout_summary_filepath, 'w', encoding='utf-8') as wf:
            writer = csv.DictWriter(wf, fieldnames=csv_fieldnames_workout_summary)
            writer.writeheader()

            for record in summary.collect():
                writer.writerow(record.to_dict())


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description='Generates workout summary (similar to activity summary).')

    workout_summary_path = f"{args.csv_workout_directory}/workout-summary.csv"
    create_workout_summary_file(args.csv_workout_path, workout_summary_path, always_true)
