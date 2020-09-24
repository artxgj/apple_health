from collections import namedtuple
from typing import Dict, List
import csv

from cls_sample_summary import (SampleSummary,
                                CumulativeQuantitySampleSummary,
                                DiscreteQuantitySampleSummary)

from cls_healthkit import HKRecordFactory
from utils import is_device_watch
import constants_apple_health_data as hd

CsvIOQuantitySamples = namedtuple('CsvIOQuantitySamples', ('input_file', 'output_file', 'output_fieldnames'))

quantity_sample_types: Dict[str, SampleSummary] = {
    'CumulativeQuantitySampleSummary': CumulativeQuantitySampleSummary,
    'DiscreteQuantitySampleSummary': DiscreteQuantitySampleSummary
}

_value_field_map = {
    hd.HK_REC_TYPE_BodyMass: hd.csv_body_mass,
    hd.HK_REC_TYPE_WaistCircumference: hd.csv_waist,
    hd.HK_REC_TYPE_VO2Max: hd.csv_vo2max,
    hd.HK_REC_TYPE_StepCount: hd.csv_step_count,
    hd.HK_REC_TYPE_DistanceWalkingRunning: hd.csv_movement_distance,
    hd.HK_REC_TYPE_RestingHeartRate: hd.csv_resting_heart_rate
}


def create_sample_summary_file(
        quantity_sample_type: str,
        csv_input_filepath: str,
        csv_output_filepath: str,
        csv_output_fieldnames: List[str]):

    if quantity_sample_type not in quantity_sample_types:
        raise ValueError(f"{quantity_sample_type} is not a valid type.")

    with open(csv_input_filepath, "r", encoding='utf-8') as rf:
        reader = csv.DictReader(rf)
        summary = None
        try:
            record = HKRecordFactory.create(next(reader))
            summary = quantity_sample_types[quantity_sample_type](record.type, record.unit)

            if is_device_watch(record.device):
                summary.tally(record)

            for row in reader:
                record = HKRecordFactory.create(row)
                if is_device_watch(record.device):
                    summary.tally(record)

        except StopIteration:
            pass

    if summary is not None:
        with open(csv_output_filepath, 'w', encoding='utf-8') as wf:
            writer = csv.DictWriter(wf, fieldnames=csv_output_fieldnames)
            writer.writeheader()

            for record in summary.collect():
                writer.writerow({
                    hd.csv_date: record.date,
                    _value_field_map[record.type]: record.value,
                    hd.csv_unit: record.unit
                })
                # writer.writerow(record.to_dict())


def create_cumulative_sample_summary_file(workout_csv_filepath: str, workout_summary_filepath: str,
                                          fieldnames: List[str]):
    create_sample_summary_file('CumulativeQuantitySampleSummary', workout_csv_filepath, workout_summary_filepath,
                               fieldnames)


def create_discrete_sample_summary_file(workout_csv_filepath: str, workout_summary_filepath: str,
                                        fieldnames: List[str]):
    create_sample_summary_file('DiscreteQuantitySampleSummary', workout_csv_filepath, workout_summary_filepath,
                               fieldnames)




