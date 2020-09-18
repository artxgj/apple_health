import argparse
import pathlib

from constants_apple_health_data import (csv_fieldnames_distance_walking_running_summary,
                                         csv_fieldnames_step_count_summary)

from summary_quantity_sample import create_cumulative_sample_summary_file, CsvIOQuantitySamples

csv_io_configs = [
    CsvIOQuantitySamples('distance-walking-running.csv', 'distance-walking-running-summary.csv',
                         csv_fieldnames_distance_walking_running_summary),
    CsvIOQuantitySamples('step-count.csv', 'step-count-summary.csv',
                         csv_fieldnames_step_count_summary),
]


def generate_cumulative_sample_files(csv_directory: str):
    for csv_io in csv_io_configs:
        csv_file_path = f"{csv_directory}/{csv_io.input_file}"
        csv_summary_path = f"{csv_directory}/{csv_io.output_file}"
        print(f"Generating {csv_summary_path}.")
        create_cumulative_sample_summary_file(csv_file_path, csv_summary_path, csv_io.output_fieldnames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__,
                                     description='Generates summary datasets of cumulative quantity sample types.')

    parser.add_argument('-csv-directory', type=str, required=True, help='directory of csv files')
    args = parser.parse_args()

    csv_folder = pathlib.Path(args.csv_directory)

    if not csv_folder.exists() or not csv_folder.is_dir():
        raise SystemExit(f"{args.csv_directory} is not a folder or it doesn't exist.")

    generate_cumulative_sample_files(args.csv_directory)


