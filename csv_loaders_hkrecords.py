from collections import namedtuple
from datetime import datetime
from typing import Sequence
import argparse
import csv
import pathlib
import sys

from myhelpers import SimplePublisher, date_in_month_predicate, ymd_path_str
import healthdata as hd
import healthkit as hk

ExportRecordCsvConfig = namedtuple('ExportRecordCsvConfig', ('type', 'name', 'fieldnames'))


def load_csvs(export_xml_path: str, output_folder_path: str, csv_loaders_config: Sequence[ExportRecordCsvConfig],
              year, month):

    hk_rec_pub = SimplePublisher(set([config.type for config in csv_loaders_config]))
    within_month_range = date_in_month_predicate(year, month)

    try:
        outfiles = []
        for config in csv_loaders_config:
            outfile = open(f'{output_folder_path}/{config.name}.csv', 'w', encoding='utf-8')
            wrtr = csv.DictWriter(outfile, fieldnames=config.fieldnames)
            wrtr.writeheader()
            hk_rec_pub.register(config.type, wrtr.writerow)
            outfiles.append(outfile)

        for elem_attr in hd.health_elem_attrs(export_xml_path, hd.is_elem_record):
            if within_month_range(datetime.strptime(elem_attr['startDate'], hk.HK_APPLE_DATETIME_FORMAT)):
                hk_rec_pub.dispatch(elem_attr['type'], elem_attr)

    finally:
        for f in outfiles:
            f.close()


if __name__ == '__main__':
    csv_loaders_config = [
        ExportRecordCsvConfig(hd.HK_REC_TYPE_ActiveEnergyBurned,
                              'active-energy-burned',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_StepCount,
                              'step-count',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_DistanceWalkingRunning,
                              'distance-walking-running',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_AppleExerciseTime,
                              'exercise-time',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_VO2Max,
                              'vo2max',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_RestingHeartRate,
                              'resting-heart-rate',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_BodyMass,
                              'body-mass',
                              hd.Fieldnames_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_WaistCircumference,
                              'waist-circumference',
                              hd.Fieldnames_Record),
    ]

    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description='loads monthly selected Record elements from exported xml file.')

    parser.add_argument('-x', '--xml', type=str, required=True, help='Apple Health exported xml filepath')
    parser.add_argument('-f', '--folder-path', type=str, required=True, help='folder path for output csv files')
    parser.add_argument('-y', '--year', type=int, required=True, help='year of records to be loaded')
    parser.add_argument('-m', '--month', type=int, required=True,
                        help='month of records to be loaded.')
    args = parser.parse_args()

    if args.month < 1 or args.month > 12:
        sys.exit(f"{args.month} is not a valid month.")

    csv_folder_path = pathlib.Path(f"{args.folder_path}/{ymd_path_str(args.year, args.month)}/Record")

    if not csv_folder_path.exists():
        csv_folder_path.mkdir(parents=True)
    elif not csv_folder_path.is_dir():
        sys.exit(f"{csv_folder_path.absolute()} is not a folder.")

    load_csvs(export_xml_path=args.xml,
              output_folder_path=csv_folder_path.absolute(),
              csv_loaders_config=csv_loaders_config,
              year=args.year, month=args.month)
