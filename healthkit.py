from dataclasses import dataclass
from typing import Dict


@dataclass
class HKRecord:
    _type: str
    _unit: str
    _value: str
    _source_name: str
    _source_version: str
    _device: str
    _creation_date: str
    _start_date: str
    _end_date: str

    @property
    def type(self):
        return self._type

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    @property
    def source_name(self):
        return self._source_name

    @property
    def source_version(self):
        return self._source_version

    @property
    def device(self):
        return self._device

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date


class HKRecordQuantityTypeIdentifier(HKRecord):
    def __init__(self,
                 type: str,
                 unit: str,
                 value: str,
                 source_name: str,
                 source_version: str,
                 device: str,
                 creation_date: str,
                 start_date: str,
                 end_date: str):
        super().__init__(
            type,
            unit,
            value,
            source_name,
            source_version,
            device,
            creation_date,
            start_date,
            end_date
        )

        self._value = float(self._value)


class HKRecordFactory:
    _HKRecordTypes = {
        'HKCategoryTypeIdentifierAppleStandHour': HKRecord,
        'HKCategoryTypeIdentifierAudioExposureEvent': HKRecord,
        'HKCategoryTypeIdentifierSleepAnalysis': HKRecord,
        'HKQuantityTypeIdentifierActiveEnergyBurned': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierAppleExerciseTime': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierAppleStandTime': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierBasalEnergyBurned': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierBloodPressureDiastolic': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierBloodPressureSystolic': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierBodyFatPercentage': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierBodyMass': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierBodyMassIndex': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierDietaryCholesterol': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierDistanceWalkingRunning': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierEnvironmentalAudioExposure': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierFlightsClimbed': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierHeadphoneAudioExposure': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierHeartRate': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierHeartRateVariabilitySDNN':HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierHeight': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierLeanBodyMass': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierRestingHeartRate': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierStepCount': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierVO2Max': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierWaistCircumference': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierWalkingHeartRateAverage': HKRecordQuantityTypeIdentifier
    }

    @staticmethod
    def create_from_xml_elem_attr(attr: Dict[str, str]) -> HKRecord:
        try:
            return HKRecordFactory._HKRecordTypes[attr['type']](
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
        except KeyError:
            raise ValueError(f"{type} is not supported.")


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
    def create_from_xml_elem_attr(cls, attr: Dict[str, str]) -> 'HKWorkout':
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
    def create_from_xml_elem_attr(cls, attr: Dict[str, str]) -> 'HKActivitySummary':
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
