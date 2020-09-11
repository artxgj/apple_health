import datetime
import pathlib

from csv_loader_argparser import parse_cmdline
from myhelpers import date_in_month_predicate, ymd_path_str
from healthkit import HK_APPLE_DATETIME_FORMAT
from hkxmlcsv import HKWorkoutXmlCsvDictWriter, AppleHealthDataReaderContextManager
import healthdata as hd


def load_csv(export_xml_path: str,
              output_folder_path: str,
              year: int,
              month: int):
    csv_path = f'{output_folder_path}/workouts.csv'

    within_month_range = date_in_month_predicate(year, month)
    with HKWorkoutXmlCsvDictWriter(csv_path, hd.Fieldnames_Workout_Csv) as wrtr, \
            AppleHealthDataReaderContextManager(export_xml_path) as rdr:
        for elem in rdr.read():
            if hd.is_elem_workout(elem):
                start_date = datetime.datetime.strptime(elem.attrib['startDate'], HK_APPLE_DATETIME_FORMAT)
                if within_month_range(start_date):
                    wrtr.write_xml_elem(elem)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description='loads and transforms Workout elements from exported xml file to a csv file.')

    load_csv(export_xml_path=args.export_xml_path,
             output_folder_path=args.csv_folder_path,
             year=args.year,
             month=args.month)
