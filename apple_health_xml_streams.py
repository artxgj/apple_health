import xml.etree.ElementTree as et

from healthdata import *


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
        self._active_summary_found = False

    def __next__(self):
        while True:
            elem = super().__next__()
            if elem.tag == ACTIVE_SUMMARY:
                self._active_summary_found = True
                return elem
            elif self._active_summary_found:
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


class AppleHealthDataBodyMassStream(AppleHealthDataRecordStream):
    def __init__(self, xml_filepath: str):
        super().__init__(xml_filepath)
        self._body_mass_found = False

    def __next__(self):
        while True:
            elem = super().__next__()
            record = elem.get(FIELD_TYPE, '')
            if record == HK_REC_TYPE_BodyMass:
                self._body_mass_found = True
                return elem
            elif self._body_mass_found:
                raise StopIteration
