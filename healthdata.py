from typing import Callable, Dict, Generator
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET


Headers_Record = [
    'type', 
    'unit', 
    'value', 
    'sourceName', 
    'sourceVersion',
    'device', 
    'creationDate', 
    'startDate', 
    'endDate']

Headers_ExportData = ['value']

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

Headers_ActivitySummary = [
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

Headers_ClinicalRecord = [
    'type',
    'identifier',
    'sourceName',
    'sourceURL',
    'fhirVersion',
    'receivedDate',
    'resourceFilePath',
]

Headers_Correlation = [
    'type',
    'sourceName',
    'sourceVersion',
    'device',
    'creationDate',
    'startDate',
    'endDate',
]


def get_health_elem(xml_filepath: str) -> Element:
    for event, elem in ET.iterparse(xml_filepath, events=("end",)):
        if event == "end":
            yield elem
            elem.clear()


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


def health_elem_attrs(apple_health_export_filepath: str, elem_predicate: Callable[[Element], bool]) \
        -> Generator[Dict[str, str], None, None]:
    return (elem.attrib for elem in get_health_elem(apple_health_export_filepath) if elem_predicate(elem))
