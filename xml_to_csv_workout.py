import csv
import datetime
import pathlib

from apple_health_xml_streams import AppleHealthDataWorkoutStream
from healthdata import *
from utils import workout_element_to_dict, localize_dates_health_data, between_dates_predicate, is_device_watch

from xml_to_csv_argparser import parse_cmdline


def xml_to_csv(xml_file_path: str,
               csv_filepath: str,
               start_date: datetime.datetime,
               end_date: datetime.datetime,
               sort_data: bool,
               watch_only_data: bool):

    with open(csv_filepath, 'w', encoding='utf-8') as outf, \
            AppleHealthDataWorkoutStream(xml_file_path) as wstream:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_Workout_Csv)
        wrtr.writeheader()

        in_date_boundary = between_dates_predicate(start_date, end_date)
        workout_dict = map(workout_element_to_dict, wstream)
        localized_workout_dict = map(localize_dates_health_data, workout_dict)

        dates_bounded_workouts = filter(lambda row: in_date_boundary(row[FIELD_START_DATE]),
                                        localized_workout_dict)

        unsorted_workouts = filter(lambda row: is_device_watch(row[FIELD_DEVICE]), dates_bounded_workouts) \
            if watch_only_data else dates_bounded_workouts

        workouts = sorted(unsorted_workouts, key=lambda row: row[FIELD_START_DATE]) if sort_data else unsorted_workouts

        for row in workouts:
            wrtr.writerow(row)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts Workout data from Apple Health Data xml file.")

    xml_to_csv(args.xml_filepath, args.csv_filepath,
               args.start_date, args.end_date,
               args.sort, args.watch_only_data)
