from collections import namedtuple
from typing import List
import argparse
import csv
import pathlib

from apple_health_xml_streams import AppleHealthDataBodyMassStream
from healthdata import FIELD_VALUE, FIELD_UNIT, FIELD_DATE, FIELD_START_DATE, Fieldnames_DailyRecordTotals
from utils import localize_apple_health_datetime_str

WeightRecord = namedtuple("WeightRecord", ('value', 'unit', 'date'))


def extract_weight_history(xml_file_path: str) -> List[WeightRecord]:
    history: List[WeightRecord] = []

    with AppleHealthDataBodyMassStream(xml_file_path) as body_mass:
        for elem in body_mass:
            history.append(WeightRecord(elem.attrib[FIELD_VALUE],
                                        elem.attrib[FIELD_UNIT],
                                        localize_apple_health_datetime_str(elem.attrib[FIELD_START_DATE])))

    history.sort(key=lambda x: x.date)
    return history


def write_csv(csv_filepath: str, weight_history: List[WeightRecord]):
    with open(csv_filepath, 'w', encoding='utf-8') as outf:
        wrtr = csv.DictWriter(outf, fieldnames=Fieldnames_DailyRecordTotals)
        wrtr.writeheader()
        
        for wh in weight_history:
            wrtr.writerow({
                FIELD_DATE: wh.date,
                FIELD_VALUE: wh.value,
                FIELD_UNIT: wh.unit
            })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=pathlib.PurePath(__file__).name,
                                     description="Extract weight (body mass) history from Apple Health Data xml file.")

    parser.add_argument('-x', '--xml-filepath', type=str, required=True, help='path of Apple Health Data xml')
    parser.add_argument('-c', '--csv-filepath', type=str, required=True, help='path of output csv file')
    args = parser.parse_args()

    xml_filepath = pathlib.Path(args.xml_filepath)

    if not xml_filepath.exists():
        raise ValueError(f'{args.xml_filepath} does not exist.')

    weight_history = extract_weight_history(args.xml_filepath)
    write_csv(args.csv_filepath, weight_history)
