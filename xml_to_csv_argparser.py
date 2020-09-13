from collections import namedtuple
import argparse
import pathlib

XmlCsvArgs = namedtuple('XmlCsvArgs', ('xml_filepath', 'csv_filepath'))


def parse_cmdline(prog: str, description: str):
    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument('-x', '--xml-filepath', type=str, required=True, help='path of Apple Health Data xml')
    parser.add_argument('-c', '--csv-filepath', type=str, required=True, help='path of output csv file')
    args = parser.parse_args()

    xml_filepath = pathlib.Path(args.xml_filepath)

    if not xml_filepath.exists():
        raise ValueError(f'{args.xml_filepath} does not exist.')

    return XmlCsvArgs(xml_filepath, args.csv_filepath)
