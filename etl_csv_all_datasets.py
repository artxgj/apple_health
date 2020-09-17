from collections import namedtuple
import argparse
import pathlib

from cls_apple_health_etl_csv import *


DatasetConfig = namedtuple('DatasetConfig', ('filename', 'etl_csv_class'))

_configs = [
    DatasetConfig(filename='active-energy-burned.csv', etl_csv_class=AppleHealthActiveEnergyBurnedETLCsv),
    DatasetConfig(filename='activity-summary.csv', etl_csv_class=AppleHealthActivitySummaryETLCsv),
    DatasetConfig(filename='body-mass.csv', etl_csv_class=AppleHealthBodyMassETLCsv),
    DatasetConfig(filename='distance-walking-running.csv', etl_csv_class=AppleHealthDistanceWalkingRunningETLCsv),
    DatasetConfig(filename='exercise-time.csv', etl_csv_class=AppleHealthExerciseTimeETLCsv),
    DatasetConfig(filename='resting-heart-rate.csv', etl_csv_class=AppleHealthRestingHeartRateETLCsv),
    DatasetConfig(filename='step-count.csv', etl_csv_class=AppleHealthStepCountETLCsv),
    DatasetConfig(filename='vo2max.csv', etl_csv_class=AppleHealthVo2MaxETLCsv),
    DatasetConfig(filename='waist-2pi-r.csv', etl_csv_class=AppleHealthWaist2PiR_ETLCsv),
    DatasetConfig(filename='workout.csv', etl_csv_class=AppleHealthWorkoutETLCsv)
]


def generate_datasets(xml_filepath: str,
                      csv_folder: str,
                      start_date: Optional[str],
                      end_date: Optional[str],
                      sort_data: bool,
                      watch_only_data: bool):
    for config in _configs:
        csv_filepath = f"{csv_folder}/{config.filename}"
        etl = config.etl_csv_class(xml_filepath, csv_filepath, start_date, end_date, watch_only_data)
        print(f"ETL for {csv_filepath}")
        try:
            etl.serialize(sort_data)
        except Exception as e:
            print(f"{e}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='generates csv datasets from exported Apple Health xml file.')

    parser.add_argument('-xml-filepath',  type=str, required=True, help='Apple Health Data xml file path')
    parser.add_argument('-csv-dest-path', type=str, required=True, help='csv folder; '
                                                                        'it will be created if it does not exist.')
    parser.add_argument('-begin-date', type=str, help='earliest date of the data to be loaded; '
                                                      'default is 1970-01-01. Format: yyyy-mm-dd')
    parser.add_argument('-end-date', type=str, help='the end date of the data to be loaded; '
                                                    'default is current date and time. Format: yyyy-mm-dd')
    parser.add_argument('-watch-only-data', action='store_true', default=False, help='load only watch-generated data')
    parser.add_argument('-sort', action='store_true', default=False, help='sort before saving to csv')

    args = parser.parse_args()
    xml_filepath = pathlib.Path(args.xml_filepath)

    if not xml_filepath.exists() or not xml_filepath.is_file():
        raise SystemExit(f"{xml_filepath} is not a regular file or it does not exist.")

    csv_folder = pathlib.Path(args.csv_dest_path)

    if not csv_folder.exists():
        csv_folder.mkdir()
    elif not csv_folder.is_dir():
        raise SystemExit(f"{args.csv_dest_path} is not a directory.")

    generate_datasets(xml_filepath, csv_folder, args.begin_date, args.end_date, args.sort, args.watch_only_data)
