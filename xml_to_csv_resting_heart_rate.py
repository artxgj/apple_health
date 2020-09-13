import pathlib

from healthdata import HK_REC_TYPE_RestingHeartRate
from xml_to_csv_argparser import parse_cmdline
from xml_to_csv_record import extract_record_type_history, write_csv


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts VO2 max history from Apple Health Data xml file.")

    history = extract_record_type_history(args.xml_filepath, HK_REC_TYPE_RestingHeartRate)
    write_csv(args.csv_filepath, history)
