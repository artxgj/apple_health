import pathlib

from apple_health_etl_csv import AppleHealthVo2MaxETLCsv
from xml_to_csv_argparser import parse_cmdline


if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts VO2 max history from Apple Health Data xml file.")

    loader = AppleHealthVo2MaxETLCsv(
        args.xml_filepath, args.csv_filepath,
        args.start_date, args.end_date,
        args.watch_only_data)

    loader.serialize(args.sort)
