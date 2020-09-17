import xml.etree.ElementTree as et

from constants_apple_health_data import *

__all__ = [
    'AppleHealthDataElementsStream',
    'AppleHealthDataActivitySummaryStream',
    'AppleHealthDataRecordStream',
    'AppleHealthDataRecordTypeStream',
    'AppleHealthDataWorkoutStream'
]


class XmlStream:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._context = None
        self._root = None
        self._context = et.iterparse(self._filepath, events=("start", "end"))
        self._clear_root: bool = False
        event, self._root = next(self._context)

    def __enter__(self):
        return self

    def __next__(self):
        if self._clear_root:
            self._root.clear()
            self._clear_root = False

        while True:
            event, elem = next(self._context)
            if event == "end":
                self._clear_root = True
                break

        return elem

    def __iter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._context = None


class AppleHealthDataElementsStream(XmlStream):
    """Returns the child elements of the root HealthData

        The receiver of a child element can use the child to retrieve
        the child's children.
    """
    def __next__(self):
        while True:
            elem = super().__next__()
            if elem.tag in HEALTH_ROOT_CHILDREN:
                return elem


class AppleHealthDataActivitySummaryStream(AppleHealthDataElementsStream):
    def __init__(self, xml_filepath: str):
        super().__init__(xml_filepath)
        self._activity_summary_found = False

    def __next__(self):
        while True:
            elem = super().__next__()
            if elem.tag == ACTIVITY_SUMMARY:
                self._activity_summary_found = True
                return elem
            elif self._activity_summary_found:
                raise StopIteration


class AppleHealthDataRecordStream(AppleHealthDataElementsStream):
    def __init__(self, xml_filepath: str):
        super().__init__(xml_filepath)
        self._record_found = False

    def __next__(self):
        while True:
            elem = super().__next__()
            if elem.tag == RECORD:
                self._record_found = True
                return elem
            elif self._record_found:
                raise StopIteration

    @staticmethod
    def is_supported_record_type(record_type: str):
        return record_type in {
            'HKCategoryTypeIdentifierAppleStandHour',
            'HKCategoryTypeIdentifierAudioExposureEvent',
            'HKCategoryTypeIdentifierSleepAnalysis',
            'HKQuantityTypeIdentifierActiveEnergyBurned',
            'HKQuantityTypeIdentifierAppleExerciseTime',
            'HKQuantityTypeIdentifierAppleStandTime',
            'HKQuantityTypeIdentifierBasalEnergyBurned',
            'HKQuantityTypeIdentifierBloodPressureDiastolic',
            'HKQuantityTypeIdentifierBloodPressureSystolic',
            'HKQuantityTypeIdentifierBodyFatPercentage',
            'HKQuantityTypeIdentifierBodyMass',
            'HKQuantityTypeIdentifierBodyMassIndex',
            'HKQuantityTypeIdentifierDietaryCholesterol',
            'HKQuantityTypeIdentifierDistanceWalkingRunning',
            'HKQuantityTypeIdentifierEnvironmentalAudioExposure',
            'HKQuantityTypeIdentifierFlightsClimbed',
            'HKQuantityTypeIdentifierHeadphoneAudioExposure',
            'HKQuantityTypeIdentifierHeartRate',
            'HKQuantityTypeIdentifierHeartRateVariabilitySDNN',
            'HKQuantityTypeIdentifierHeight',
            'HKQuantityTypeIdentifierLeanBodyMass',
            'HKQuantityTypeIdentifierRestingHeartRate',
            'HKQuantityTypeIdentifierStepCount',
            'HKQuantityTypeIdentifierVO2Max',
            'HKQuantityTypeIdentifierWaistCircumference',
            'HKQuantityTypeIdentifierWalkingHeartRateAverage'
        }


class AppleHealthDataRecordTypeStream(AppleHealthDataElementsStream):
    def __init__(self, xml_filepath: str, record_type: str):
        super().__init__(xml_filepath)

        if not AppleHealthDataRecordStream.is_supported_record_type(record_type):
            raise ValueError(f'{record_type} is not supported.')

        self._record_type = record_type
        self._record_type_found = False

    def __next__(self):
        while True:
            elem = super().__next__()
            record = elem.get(FIELD_TYPE, '')
            if record == self._record_type:
                self._record_type_found = True
                return elem
            elif self._record_type_found:
                # records of the same record type appear to be
                # clustered together in the xml file; stop processing
                # when the record type is read
                raise StopIteration


class AppleHealthDataWorkoutStream(AppleHealthDataElementsStream):
    def __init__(self, xml_filepath: str):
        super().__init__(xml_filepath)
        self._workout_found = False

    def __next__(self):
        while True:
            elem = super().__next__()
            if elem.tag == WORKOUT:
                self._workout_found = True
                return elem
            elif self._workout_found:
                raise StopIteration


