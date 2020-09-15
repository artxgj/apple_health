import pathlib

from etl_csv_argparser import parse_cmdline
from apple_health_etl_csv import AppleHealthActiveEnergyBurnedETLCsv

if __name__ == '__main__':
    args = parse_cmdline(prog=pathlib.PurePath(__file__).name,
                         description="Extracts VO2 max history from Apple Health Data xml file.")

    csv_loader = AppleHealthActiveEnergyBurnedETLCsv(
        args.xml_filepath, args.csv_filepath,
        args.start_date, args.end_date,
        args.watch_only_data)

    csv_loader.serialize(args.sort)
