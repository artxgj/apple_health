from typing import Dict, Union
import csv

from cls_sample_summary import (QuantitySampleSummaryRecord,
                                SampleSummary,
                                CumulativeQuantitySampleSummary,
                                DiscreteQuantitySampleSummary)
from healthkit import HKRecordFactory
from utils import is_device_watch


quantity_sample_types: Dict[str, SampleSummary] = {
    'CumulativeQuantitySampleSummary': CumulativeQuantitySampleSummary,
    'DiscreteQuantitySampleSummary': DiscreteQuantitySampleSummary
}


def create_sample_summary_file(
        quantity_sample_type: str,
        workout_csv_filepath: str,
        workout_summary_filepath: str):

    if quantity_sample_type not in quantity_sample_types:
        raise ValueError(f"{quantity_sample_type} is not a valid type.")

    with open(workout_csv_filepath, "r", encoding='utf-8') as rf:
        reader = csv.DictReader(rf)
        summary = None
        try:
            record = HKRecordFactory.create(next(reader))
            summary = quantity_sample_types[quantity_sample_type](record.unit)

            if is_device_watch(record.device):
                summary.tally(record)

            for row in reader:
                record = HKRecordFactory.create(row)
                if is_device_watch(record.device):
                    summary.tally(record)

        except StopIteration:
            pass

    if summary is not None:
        with open(workout_summary_filepath, 'w', encoding='utf-8') as wf:
            writer = csv.DictWriter(wf, fieldnames=QuantitySampleSummaryRecord.field_names())
            writer.writeheader()

            for record in summary.collect():
                writer.writerow(record.to_dict())


def create_cumulative_sample_summary_file(workout_csv_filepath: str, workout_summary_filepath: str):
    create_sample_summary_file('CumulativeQuantitySampleSummary', workout_csv_filepath, workout_summary_filepath)


def create_discrete_sample_summary_file(workout_csv_filepath: str, workout_summary_filepath: str):
    create_sample_summary_file('DiscreteQuantitySampleSummary', workout_csv_filepath, workout_summary_filepath)




