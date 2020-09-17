from collections import namedtuple
import argparse
import pathlib

from summary_quantity_sample import create_discrete_sample_summary_file

CsvIOQuantitySamples = namedtuple('CsvIOQuantitySamples', ('input_file', 'output_file'))

csv_io_configs = [
    CsvIOQuantitySamples('body-mass.csv', 'bodymass-summary.csv'),
    CsvIOQuantitySamples('vo2max.csv', 'vo2max-summary.csv'),
    CsvIOQuantitySamples('waist-2pi-r.csv', 'waist-2pi-r-summmary.csv')
]


def generate_discrete_sample_files(csv_directory: str):
    for csv_io in csv_io_configs:
        csv_file_path = f"{csv_directory}/{csv_io.input_file}"
        csv_summary_path = f"{csv_directory}/{csv_io.output_file}"
        print(f"Generating {csv_summary_path}.")
        create_discrete_sample_summary_file(csv_file_path, csv_summary_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of discrete quantity sample types.')

    parser.add_argument('-csv-directory', type=str, required=True, help='directory of csv files')
    args = parser.parse_args()

    csv_folder = pathlib.Path(args.csv_directory)

    if not csv_folder.exists() or not csv_folder.is_dir():
        raise SystemExit(f"{args.csv_directory} is not a folder or it doesn't exist.")

    generate_discrete_sample_files(args.csv_directory)
