import datetime
import pathlib

from .csv_loader_argparser import parse_cmdline
from utils import date_in_month_predicate
from healthkit import HK_APPLE_DATE_FORMAT
from .hkxmlcsv import HKXmlCsvDictWriterContextManager
from apple_health_xml_streams import AppleHealthDataActivitySummaryStream
import healthdata as hd


def load_csv(export_xml_path: str,
             output_folder_path: str,
             year: int,
             month: int):
    csv_path = f'{output_folder_path}/activity-summary.csv'
    within_month_range = date_in_month_predicate(year, month)

    with HKXmlCsvDictWriterContextManager(csv_path, hd.Fieldnames_ActivitySummary) as wrtr, \
            AppleHealthDataActivitySummaryStream(export_xml_path) as rdr:
        for elem in rdr:
            if within_month_range(datetime.datetime.strptime(f"{elem.attrib['dateComponents']}",
                                                             f"{HK_APPLE_DATE_FORMAT}")):
                wrtr.write_xml_elem(elem)


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description='loads ActivitySummary elements from exported xml file to csv files.')

    load_csv(export_xml_path=args.export_xml_path,
             output_folder_path=args.csv_folder_path,
             year=args.year,
             month=args.month)

