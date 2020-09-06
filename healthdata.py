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

Fieldnames_Record = [
    'type', 
    'unit', 
    'value', 
    'sourceName', 
    'sourceVersion',
    'device', 
    'creationDate', 
    'startDate', 
    'endDate']

Fieldnames_ExportData = ['value']

Headers_Workout = [
    'workoutActivityType',
    'duration',
    'durationUnit',
    'totalDistance',
    'totalDistanceUnit',
    'totalEnergyBurned',
    'totalEnergyBurnedUnit',
    'sourceName',
    'sourceVersion',
    'device',
    'creationDate',
    'startDate',
    'endDate',
]

Fieldnames_ActivitySummary = [
    'dateComponents',
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
    'type',
    'identifier',
    'sourceName',
    'sourceURL',
    'fhirVersion',
    'receivedDate',
    'resourceFilePath',
]

Fieldnames_Correlation = [
    'type',
    'sourceName',
    'sourceVersion',
    'device',
    'creationDate',
    'startDate',
    'endDate',
]


Fieldnames_Workout = [
    'workoutActivityType',
    'duration',
    'durationUnit',
    'totalDistance',
    'totalDistanceUnit',
    'totalEnergyBurned',
    'totalEnergyBurnedUnit',
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


def get_health_elem(xml_filepath: str, predicate: Callable[[Element], bool] = lambda e: True) -> Element:
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


def health_elem_attrs(apple_health_export_filepath: str, predicate: Callable[[Element], bool] = lambda e: True) \
        -> Generator[Dict[str, str], None, None]:
    return (elem.attrib for elem in get_health_elem(apple_health_export_filepath, predicate))
