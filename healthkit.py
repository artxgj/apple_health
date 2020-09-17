from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List

import healthdata as hd

HK_APPLE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
HK_APPLE_DATE_FORMAT = "%Y-%m-%d"
HK_APPLE_TIMEZONE = '-0700'


@dataclass
class HKWorkout:
    _workout_activity_type: str
    _duration: float
    _duration_unit: str
    _total_distance: float
    _total_distance_unit: str
    _total_energy_burned: float
    _total_energy_burned_unit: str
    _source_name: str
    _source_version: str
    _device: str
    _creation_date: str
    _start_date: str
    _end_date: str

    @classmethod
    def create(cls, attr: Dict[str, str]) -> 'HKWorkout':
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

    @property
    def workout_activity_type(self):
        return self._workout_activity_type

    @property
    def duration(self):
        return self._duration

    @property
    def duration_unit(self):
        return self._duration_unit

    @property
    def total_distance(self):
        return self._total_distance

    @property
    def total_distance_unit(self):
        return self._total_distance_unit

    @property
    def total_energy_burned(self):
        return self._total_energy_burned

    @property
    def total_energy_burned_unit(self):
        return self._total_energy_burned_unit

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


class HKWorkoutWithMetaData(HKWorkout):
    def __init__(self,
                 _workout_activity_type: str,
                 _duration: float,
                 _duration_unit: str,
                 _total_distance: float,
                 _total_distance_unit: str,
                 _total_energy_burned: float,
                 _total_energy_burned_unit: str,
                 _source_name: str,
                 _source_version: str,
                 _device: str,
                 _creation_date: str,
                 _start_date: str,
                 _end_date: str,
                 _is_indoor: bool,
                 _average_mets: str,
                 _weather_temperature: str,
                 _weather_humidity: str,
                 _timezone: str,
                 _elevation_ascended: str
                 ):
        super().__init__(_workout_activity_type,
                         _duration,
                         _duration_unit,
                         _total_distance,
                         _total_distance_unit,
                         _total_energy_burned,
                         _total_energy_burned_unit,
                         _source_name,
                         _source_version,
                         _device,
                         _creation_date,
                         _start_date,
                         _end_date
                         )
        self._is_indoor = _is_indoor
        self._average_mets = _average_mets
        self._weather_temperature = _weather_temperature
        self._weather_humidity = _weather_humidity
        self._timezone = _timezone
        self._elevation_ascended = _elevation_ascended

    @classmethod
    def create(cls, attr: Dict[str, str]) -> 'HKWorkoutWithMetaData':
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
            attr['endDate'],
            bool(int(attr['HKIndoorWorkout'])) if attr['HKIndoorWorkout'] != '' else False,
            attr['HKAverageMETs'],
            attr['HKWeatherTemperature'],
            attr['HKWeatherHumidity'],
            attr['HKTimeZone'],
            attr['HKElevationAscended']
        )

    @property
    def is_indoor(self):
        return self._is_indoor

    @property
    def average_mets(self):
        return self._average_mets

    @property
    def weather_temperature(self):
        return self._weather_temperature

    @property
    def weather_humidity(self):
        return self._weather_humidity

    @property
    def timezone(self):
        return self._timezone

    @property
    def elevation_ascended(self):
        return self._elevation_ascended


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

        self._value: float = float(self._value)


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
        'HKQuantityTypeIdentifierHeartRateVariabilitySDNN': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierHeight': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierLeanBodyMass': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierRestingHeartRate': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierStepCount': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierVO2Max': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierWaistCircumference': HKRecordQuantityTypeIdentifier,
        'HKQuantityTypeIdentifierWalkingHeartRateAverage': HKRecordQuantityTypeIdentifier
    }

    @staticmethod
    def create(attr: Dict[str, str]) -> HKRecord:
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
class HKActivitySummary:
    _date_components: str
    _active_energy_burned: float
    _active_energy_burned_goal: float
    _active_energy_burned_unit: str
    _apple_move_minutes: float
    _apple_move_minutes_goal: float
    _apple_exercise_time: float
    _apple_exercise_time_goal: float
    _apple_stand_hours: int
    _apple_stand_hours_goal: int

    @classmethod
    def create(cls, attr: Dict[str, str]) -> 'HKActivitySummary':
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

    @property
    def date_components(self):
        return self._date_components

    @property
    def active_energy_burned(self):
        return self._active_energy_burned

    @property
    def active_energy_burned_goal(self):
        return self._active_energy_burned_goal

    @property
    def active_energy_burned_unit(self):
        return self._active_energy_burned_unit

    @property
    def apple_move_minutes(self):
        return self._apple_move_minutes

    @property
    def apple_move_minutes_goal(self):
        return self._apple_move_minutes_goal

    @property
    def apple_exercise_time(self):
        return self._apple_exercise_time

    @property
    def apple_exercise_time_goal(self):
        return self._apple_exercise_time_goal

    @property
    def apple_stand_hours(self):
        return self._apple_stand_hours

    @property
    def apple_stand_hours_goal(self):
        return self._apple_stand_hours_goal

