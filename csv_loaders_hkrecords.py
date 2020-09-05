from collections import namedtuple
from typing import Sequence
import argparse
import csv
import pathlib
import sys

from myhelpers import SimplePublisher
import healthdata as hd

ExportRecordCsvConfig = namedtuple('ExportRecordCsvConfig', ('type', 'name', 'fieldnames'))


def load_csvs(export_xml_path: str, output_folder_path: str, csv_loaders_config: Sequence[ExportRecordCsvConfig]):
    hk_rec_pub = SimplePublisher(set([config.type for config in csv_loaders_config]))

    try:
        outfiles = []
        for config in csv_loaders_config:
            outfile = open(f'{output_folder_path}/{config.name}.csv', 'w', encoding='utf-8')
            wrtr = csv.DictWriter(outfile, fieldnames=config.fieldnames)
            hk_rec_pub.register(config.type, wrtr.writerow)
            outfiles.append(outfile)

        for elem_attr in hd.health_elem_attrs(export_xml_path, hd.is_elem_record):
            hk_rec_pub.dispatch(elem_attr['type'], elem_attr)

    finally:
        for f in outfiles:
            f.close()


if __name__ == '__main__':
    csv_loaders_config = [
        ExportRecordCsvConfig(hd.HK_REC_TYPE_ActiveEnergyBurned,
                              'active-energy-burned',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_StepCount,
                              'step-count',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_DistanceWalkingRunning,
                              'distance-walking-running',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_AppleExerciseTime,
                              'exercise-time',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_VO2Max,
                              'vo2max',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_RestingHeartRate,
                              'resting-heart-rate',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_BodyMass,
                              'body-mass',
                              hd.Headers_Record),
        ExportRecordCsvConfig(hd.HK_REC_TYPE_WaistCircumference,
                              'waist-circumference',
                              hd.Headers_Record),
    ]

    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description='loads selected Record elements from exported xml file to csv files.')

    parser.add_argument('-x', '--xml', type=str, required=True, help='Apple Health exported xml filepath')
    parser.add_argument('-f', '--folder-path', type=str, required=True, help='folder path for output csv files')
    args = parser.parse_args()

    csv_folder_path = pathlib.Path(args.folder_path)

    if not csv_folder_path.exists():
        csv_folder_path.mkdir(parents=True)
    elif not csv_folder_path.is_dir():
        sys.exit(f"{csv_folder_path.absolute()} is not a folder.")

    load_csvs(export_xml_path=args.xml,
              output_folder_path=csv_folder_path.absolute(),
              csv_loaders_config=csv_loaders_config)
