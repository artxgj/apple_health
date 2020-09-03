from dataclasses import dataclass
from typing import Dict


@dataclass
class HKRecord:
    type: str
    unit: str
    value: str
    source_name: str
    source_version: str
    device: str
    creation_date: str
    start_date: str
    end_date: str

    @classmethod
    def from_xml_elem_attr(cls, attr: Dict[str, str]):
        return cls(
            attr['type'],
            attr.get('unit', ''),
            attr.get('value', ''),
            attr['sourceName'],
            attr.get('sourceVersion', ''),
            attr.get('device', ''),
            attr.get('creationDate', ''),
            attr['startDate'],
            attr['endDate']
        )


@dataclass
class HKWorkout:
    workoutActivityType: str
    duration: float
    durationUnit: str
    total_distance: float
    total_distance_unit: str
    total_energy_burned: float
    total_energy_burned_unit: str
    source_name: str
    source_version: str
    device: str
    creation_date: str
    start_date: str
    end_date: str

    @classmethod
    def from_xml_elem_attr(cls, attr: Dict[str, str]):
        return cls(
            attr['workoutActivityType'],
            float(attr.get('duration', 0.0)),
            attr.get('durationUnit', ''),
            float(attr.get('totalDistance', 0.0)),
            attr.get('totalDistanceUnit', ''),
            float(attr.get('totalEnergyBurned', 0.0)),
            attr.get('totalEnergyBurnedUnit', ''),
            attr['sourceName'],
            attr.get('sourceVersion', ''),
            attr.get('device', ''),
            attr.get('creationDate', ''),
            attr['startDate'],
            attr['endDate']
        )


@dataclass
class HKActivitySummary:
    date_components: str
    active_energy_burned: float
    active_energy_burned_goal: float
    active_energy_burnedUnit: str
    apple_move_minutes: float
    apple_move_minutes_goal: float
    apple_exercise_time: float
    apple_exercise_time_goal: float
    apple_stand_hours: int
    apple_stand_hours_goal: int

    @classmethod
    def from_xml_elem_attr(cls, attr: Dict[str, str]):
        return cls(
            attr.get('dateComponents', ''),
            float(attr.get('activeEnergyBurned', 0.0)),
            float(attr.get('activeEnergyBurnedGoal', 0.0)),
            attr.get('activeEnergyBurnedUnit', ''),
            float(attr.get('appleMoveMinutes', 0.0)),
            float(attr.get('appleMoveMinutesGoal', 0.0)),
            float(attr.get('appleExerciseTime', 0.0)),
            float(attr.get('appleExerciseTimeGoal', 0.0)),
            int(attr.get('appleStandHours', 0)),
            int(attr.get('appleStandHoursGoal', 0))
        )
