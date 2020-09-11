from collections import namedtuple
from datetime import datetime
from typing import Sequence
import pathlib

from csv_loader_argparser import parse_cmdline
from utils import SimplePublisher, date_in_month_predicate, ymd_path_str
from hkxmlcsv import HKRecordXmlCsvDictWriter, AppleHealthDataReaderContextManager
import healthdata as hd
import healthkit as hk


ExportRecordCsvConfig = namedtuple('ExportRecordCsvConfig', ('type', 'name', 'fieldnames'))


def load_csvs(export_xml_path: str,
              output_folder_path: str,
              year: int, month: int,
              csv_loaders_config: Sequence[ExportRecordCsvConfig]):

    hk_rec_pub = SimplePublisher(set([config.type for config in csv_loaders_config]))
    within_month_range = date_in_month_predicate(year, month)

    try:
        record_writers = []
        for config in csv_loaders_config:
            hk_rec_wrtr = HKRecordXmlCsvDictWriter(f'{output_folder_path}/{config.name}.csv', fieldnames=config.fieldnames)
            hk_rec_pub.register(config.type, hk_rec_wrtr.write_xml_elem)
            record_writers.append(hk_rec_wrtr)

        with AppleHealthDataReaderContextManager(export_xml_path) as rec_stream:
            for elem in rec_stream.read():
                if hd.is_elem_record(elem):
                    if within_month_range(datetime.strptime(elem.attrib['startDate'], hk.HK_APPLE_DATETIME_FORMAT)):
                        hk_rec_pub.dispatch(elem.attrib['type'], elem)

    finally:
        for rw in record_writers:
            rw.close()


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

    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description='loads and transforms Record elements from exported xml file to csv files.')

    load_csvs(export_xml_path=args.export_xml_path,
              output_folder_path=args.csv_folder_path,
              year=args.year,
              month=args.month,
              csv_loaders_config=csv_loaders_config)

