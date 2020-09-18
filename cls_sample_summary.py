from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List

from cls_healthkit import HKWorkout, HKRecord
import constants_apple_health_data as hd


class SampleSummary(ABC):
    """SampleSummary tallies daily summary of a quantity. It mimics Apple Health's ActivitySummary xml element.
    """

    @abstractmethod
    def tally(self, Any):
        pass

    @abstractmethod
    def collect(self) -> List[Any]:
        pass


@dataclass
class _WorkoutQuantitiesTally:
    duration: float
    total_distance: float
    total_energy_burned: float

    def __add__(self, other):
        self.duration += other.duration
        self.total_distance += other.total_distance
        self.total_energy_burned += other.total_energy_burned


@dataclass
class WorkoutSummaryRecord:
    date: str
    duration: float
    duration_unit: str
    total_distance: float
    total_distance_unit: str
    total_energy_burned: float
    total_energy_burned_unit: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            hd.csv_date: self.date,
            hd.csv_duration: self.duration,
            hd.csv_duration_unit: self.duration_unit,
            hd.csv_distance: self.total_distance,
            hd.csv_distance_unit: self.total_distance_unit,
            hd.csv_energy_burned: self.total_energy_burned,
            hd.csv_energy_burned_unit: self.total_energy_burned_unit
        }


class WorkoutSummary(SampleSummary):
    """This class mimics the ActivitySummary element of Apple Health's xml file."""

    def __init__(self, duration_unit: str, distance_unit: str, energy_burned_unit):
        self._duration_unit = duration_unit
        self._energy_burned_unit = energy_burned_unit
        self._distance_unit = distance_unit
        self._tally: Dict[str, _WorkoutQuantitiesTally] = {}

    def tally(self, workout: HKWorkout):
        key = workout.start_date[:10]
        wq = _WorkoutQuantitiesTally(workout.duration, workout.total_distance, workout.total_energy_burned)
        if key not in self._tally:
            self._tally[key] = wq
        else:
            self._tally[key] + wq

    def collect(self) -> List[WorkoutSummaryRecord]:
        return [WorkoutSummaryRecord(day_of_month,
                                     wq.duration,
                                     self._duration_unit,
                                     wq.total_distance,
                                     self._distance_unit,
                                     wq.total_energy_burned,
                                     self._energy_burned_unit) for day_of_month, wq in self._tally.items()]


@dataclass
class QuantitySampleSummaryRecord:
    date: str
    type: str
    value: float
    unit: str

    @staticmethod
    def field_names():
        return [hd.FIELD_DATE, hd.FIELD_VALUE, hd.FIELD_UNIT]

    def to_dict(self) -> Dict[str, Any]:
        return {
            hd.FIELD_DATE: self.date,
            hd.FIELD_VALUE: self.value,
            hd.FIELD_UNIT: self.unit
        }


class DiscreteQuantitySampleSummary(SampleSummary):
    def __init__(self, type: str, unit: str):
        self._tally = {}
        self._items = {}
        self._unit = unit
        self._type = type

    def tally(self, record: HKRecord):
        key = record.start_date[:10]

        if key not in self._tally:
            self._tally[key] = record.value
            self._items[key] = 1
        else:
            self._tally[key] += record.value
            self._items[key] += 1

    def collect(self) -> List[QuantitySampleSummaryRecord]:
        return [QuantitySampleSummaryRecord(day_of_month, self._type, value / self._items[day_of_month], self._unit)
                for day_of_month, value in self._tally.items()]


class CumulativeQuantitySampleSummary(SampleSummary):
    def __init__(self, type: str, unit: str):
        self._type = type
        self._tally = {}
        self._unit = unit

    def tally(self, record: HKRecord):
        key = record.start_date[:10]

        if key not in self._tally:
            self._tally[key] = record.value
        else:
            self._tally[key] += record.value

    def collect(self) -> List[QuantitySampleSummaryRecord]:
        return [QuantitySampleSummaryRecord(day_of_month, self._type, value, self._unit)
                for day_of_month, value in self._tally.items()]
