import pathlib

from cls_apple_health_etl_csv import AppleHealthWaist2PiR_ETLCsv
from etl_csv_argparser import parse_cmdline

if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts Waist Circumference data from Apple Health Data xml file.")

    loader = AppleHealthWaist2PiR_ETLCsv(
        args.xml_filepath, args.csv_filepath,
        args.start_date, args.end_date,
        args.watch_only_data
    )

    loader.serialize(args.sort)
