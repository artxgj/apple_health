import pathlib

from healthdata import HK_REC_TYPE_RestingHeartRate
from xml_to_csv_argparser import parse_cmdline
from xml_to_csv_record import xml_to_csv

if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts VO2 max history from Apple Health Data xml file.")

    xml_to_csv(args.xml_filepath, args.csv_filepath,
               args.start_date, args.end_date,
               args.sort, args.watch_only_data,
               HK_REC_TYPE_RestingHeartRate)
