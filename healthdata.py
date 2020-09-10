from typing import Callable, Dict, Generator
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

HK_REC_TYPE_AppleStandHour = 'HKCategoryTypeIdentifierAppleStandHour'
HK_REC_TYPE_AudioExposureEvent = 'HKCategoryTypeIdentifierAudioExposureEvent'
HK_REC_TYPE_SleepAnalysis = 'HKCategoryTypeIdentifierSleepAnalysis'
HK_REC_TYPE_ActiveEnergyBurned = 'HKQuantityTypeIdentifierActiveEnergyBurned'
HK_REC_TYPE_AppleExerciseTime = 'HKQuantityTypeIdentifierAppleExerciseTime'
HK_REC_TYPE_AppleStandTime = 'HKQuantityTypeIdentifierAppleStandTime'
HK_REC_TYPE_BasalEnergyBurned = 'HKQuantityTypeIdentifierBasalEnergyBurned'
HK_REC_TYPE_BloodPressureDiastolic = 'HKQuantityTypeIdentifierBloodPressureDiastolic'
HK_REC_TYPE_BloodPressureSystolic = 'HKQuantityTypeIdentifierBloodPressureSystolic'
HK_REC_TYPE_BodyFatPercentage = 'HKQuantityTypeIdentifierBodyFatPercentage'
HK_REC_TYPE_BodyMass = 'HKQuantityTypeIdentifierBodyMass'
HK_REC_TYPE_BodyMassIndex = 'HKQuantityTypeIdentifierBodyMassIndex'
HK_REC_TYPE_DietaryCholesterol = 'HKQuantityTypeIdentifierDietaryCholesterol'
HK_REC_TYPE_DistanceWalkingRunning = 'HKQuantityTypeIdentifierDistanceWalkingRunning'
HK_REC_TYPE_EnvironmentalAudioExposure = 'HKQuantityTypeIdentifierEnvironmentalAudioExposure'
HK_REC_TYPE_FlightsClimbed = 'HKQuantityTypeIdentifierFlightsClimbed'
HK_REC_TYPE_HeadphoneAudioExposure = 'HKQuantityTypeIdentifierHeadphoneAudioExposure'
HK_REC_TYPE_HeartRate = 'HKQuantityTypeIdentifierHeartRate'
HK_REC_TYPE_HeartRateVariabilitySDNN = 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN'
HK_REC_TYPE_Height = 'HKQuantityTypeIdentifierHeight'
HK_REC_TYPE_LeanBodyMass = 'HKQuantityTypeIdentifierLeanBodyMass'
HK_REC_TYPE_RestingHeartRate = 'HKQuantityTypeIdentifierRestingHeartRate'
HK_REC_TYPE_StepCount = 'HKQuantityTypeIdentifierStepCount'
HK_REC_TYPE_VO2Max = 'HKQuantityTypeIdentifierVO2Max'
HK_REC_TYPE_WaistCircumference = 'HKQuantityTypeIdentifierWaistCircumference'
HK_REC_TYPE_WalkingHeartRateAverage = 'HKQuantityTypeIdentifierWalkingHeartRateAverage'

FIELD_DATE = 'dateComponents'
FIELD_VALUE = 'value'
FIELD_UNIT = 'unit'
FIELD_TYPE = 'type'

FIELD_DURATION = 'duration'
FIELD_DURATION_UNIT = 'durationUnit'
FIELD_TOTAL_DISTANCE = 'totalDistance'
FIELD_TOTAL_DISTANCE_UNIT = 'totalDistanceUnit'
FIELD_TOTAL_ENERGY_BURNED = 'totalEnergyBurned'
FIELD_TOTAL_ENERGY_BURNED_UNIT = 'totalEnergyBurnedUnit'

Fieldnames_Record = [
    FIELD_TYPE,
    FIELD_UNIT,
    FIELD_VALUE,
    'sourceName', 
    'sourceVersion',
    'device', 
    'creationDate', 
    'startDate', 
    'endDate']

Fieldnames_ExportData = ['value']

Fieldnames_ActivitySummary = [
    FIELD_DATE,
    'activeEnergyBurned',
    'activeEnergyBurnedGoal',
    'activeEnergyBurnedUnit',
    'appleMoveMinutes',
    'appleMoveMinutesGoal',
    'appleExerciseTime',
    'appleExerciseTimeGoal',
    'appleStandHours',
    'appleStandHoursGoal'
]

Fieldnames_ClinicalRecord = [
    FIELD_TYPE,
    'identifier',
    'sourceName',
    'sourceURL',
    'fhirVersion',
    'receivedDate',
    'resourceFilePath',
]

Fieldnames_Correlation = [
    FIELD_TYPE,
    'sourceName',
    'sourceVersion',
    'device',
    'creationDate',
    'startDate',
    'endDate',
]


Fieldnames_Workout = [
    'workoutActivityType',
    FIELD_DURATION,
    FIELD_DURATION_UNIT,
    FIELD_TOTAL_DISTANCE,
    FIELD_TOTAL_DISTANCE_UNIT,
    FIELD_TOTAL_ENERGY_BURNED,
    FIELD_TOTAL_ENERGY_BURNED_UNIT,
    'sourceName',
    'sourceVersion',
    'device',
    'creationDate',
    'startDate',
    'endDate'
]


Fieldnames_Workout_MetadataEntry = [
    'HKIndoorWorkout',
    'HKAverageMETs',
    'HKWeatherTemperature',
    'HKWeatherHumidity',
    'HKTimeZone',
    'HKElevationAscended'
]


Fieldnames_Workout_Csv = Fieldnames_Workout + Fieldnames_Workout_MetadataEntry


Fieldnames_DailyRecordTotals = [
    FIELD_DATE,
    FIELD_VALUE,
    FIELD_UNIT
]

Fieldnames_DailyWorkoutsTotals = [
    FIELD_DATE,
    FIELD_DURATION,
    FIELD_DURATION_UNIT,
    FIELD_TOTAL_DISTANCE,
    FIELD_TOTAL_DISTANCE_UNIT,
    FIELD_TOTAL_ENERGY_BURNED,
    FIELD_TOTAL_ENERGY_BURNED_UNIT
]


Fieldnames_DailyWorkoutsByTypes = Fieldnames_DailyWorkoutsTotals + [FIELD_TYPE]


def get_health_elem(xml_filepath: str,
                    predicate: Callable[[Element], bool] = lambda e: True) -> Element:
    """

    :param xml_filepath: Path of Apple Health's export.xml
    :param predicate: boolean function that tests an xml element.
    :return:
    """
    context = ET.iterparse(xml_filepath, events=("start", "end"))

    # get the root element
    event, root = next(context)

    for event, elem in context:
        if event == "end" and predicate(elem):
            yield elem

    root.clear()


def is_elem_record(element: Element) -> bool:
    return element.tag == 'Record'


def is_elem_workout(element: Element) -> bool:
    return element.tag == 'Workout'


def is_elem_activity_summary(element: Element) -> bool:
    return element.tag == 'ActivitySummary'


def is_elem_correlation(element: Element) -> bool:
    return element.tag == 'Correlation'


def is_elem_clinical_record(element: Element) -> bool:
    return element.tag == 'ClinicalRecord'


def health_elem_attrs(apple_health_export_filepath: str,
                      predicate: Callable[[Element], bool] = lambda e: True) \
        -> Generator[Dict[str, str], None, None]:
    return (elem.attrib for elem in get_health_elem(apple_health_export_filepath, predicate))
