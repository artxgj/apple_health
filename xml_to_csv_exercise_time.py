import pathlib

from apple_health_etl_csv import AppleHealthExerciseTimeETLCsv
from xml_to_csv_argparser import parse_cmdline


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts Exercise Time data from Apple Health Data xml file.")

    loader = AppleHealthExerciseTimeETLCsv(args.xml_filepath, args.csv_filepath, args.start_date, args.end_date,
                                           args.watch_only_data)

    loader.serialize(args.sort)
