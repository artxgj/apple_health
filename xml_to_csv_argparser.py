from dataclasses import dataclass
import argparse
import datetime
import pathlib


@dataclass
class XmlCsvArgs:
    xml_filepath: str
    csv_filepath: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    sort: bool
    watch_only_data: bool


def parse_cmdline(prog: str, description: str) -> XmlCsvArgs:
    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument('-xml-path',  type=str, required=True, help='Apple Health Data xml file path')
    parser.add_argument('-csv-path', type=str, required=True, help='csv output file path')
    parser.add_argument('-begin-date', type=str, help='earliest date of the data to be loaded')
    parser.add_argument('-end-date', type=str, help='the end date of the data to be loaded.')
    parser.add_argument('-sort', action='store_true', default=False, help='sort before saving to csv')
    parser.add_argument('-watch-only-data', action='store_true', default=False, help='load only watch-generated data')
    args = parser.parse_args()

    xml_filepath = pathlib.Path(args.xml_path)

    if not xml_filepath.exists():
        raise ValueError(f'{args.xml_path} does not exist.')

    if args.begin_date is None:
        start_date = datetime.datetime(1970, 1, 1)
    else:
        start_date = datetime.datetime.strptime(args.begin_date, "%Y-%m-%d")

    if args.end_date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(args.end_date, "%Y-%m-%d")
        end_date = end_date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

    return XmlCsvArgs(xml_filepath,
                      args.csv_path,
                      start_date,
                      end_date,
                      args.sort,
                      args.watch_only_data
                      )
