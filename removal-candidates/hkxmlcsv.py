from typing import List
import csv
import xml.etree.ElementTree as et

from utils import localize_apple_health_datetime_str
from healthdata import *


class HKXmlCsvDictWriterContextManager:
    def __init__(self, filepath: str, fieldnames: List[str]):
        self._csvfile = open(filepath, 'w', encoding='utf-8')
        self._writer = csv.DictWriter(self._csvfile, fieldnames=fieldnames)
        self._writer.writeheader()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def write_xml_elem(self, elem: et.Element):
        self._writer.writerow(elem.attrib)

    def close(self):
        self._csvfile.close()


class HKRecordXmlCsvDictWriter(HKXmlCsvDictWriterContextManager):
    def __init__(self, filepath: str, fieldnames: List[str], use_local_time: bool = True):
        super().__init__(filepath, fieldnames)
        self._use_local_time = use_local_time

    def write_xml_elem(self, elem: et.Element):
        row = elem.attrib.copy()

        if self._use_local_time:
            row[FIELD_START_DATE] = localize_apple_health_datetime_str(row[FIELD_START_DATE])
            row[FIELD_END_DATE] = localize_apple_health_datetime_str(row[FIELD_END_DATE])
            row[FIELD_CREATION_DATE] = localize_apple_health_datetime_str(row[FIELD_CREATION_DATE])

        self._writer.writerow(row)


class HKWorkoutXmlCsvDictWriter(HKXmlCsvDictWriterContextManager):
    _metadata_entry_fields = set(Fieldnames_Workout_MetadataEntry)

    def __init__(self, filepath: str, fieldnames: List[str], use_local_time: bool = True):
        super().__init__(filepath, fieldnames)
        self._use_local_time = use_local_time

    def write_xml_elem(self, elem: et.Element):
        row = elem.attrib.copy()
        kv = {mde.attrib['key']: mde.attrib['value'] for mde in elem.findall('MetadataEntry')}

        for k in HKWorkoutXmlCsvDictWriter._metadata_entry_fields:
            row[k] = kv.get(k, '')

        if self._use_local_time:
            row[FIELD_START_DATE] = localize_apple_health_datetime_str(row[FIELD_START_DATE])
            row[FIELD_END_DATE] = localize_apple_health_datetime_str(row[FIELD_END_DATE])
            row[FIELD_CREATION_DATE] = localize_apple_health_datetime_str(row[FIELD_CREATION_DATE])

        self._writer.writerow(row)

