from typing import Generator, List
import csv
import xml.etree.ElementTree as et

from utils import localize_apple_health_datetime_str
import healthdata as hd


class XmlReaderContextManager:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._context = None
        self._root = None

    def __enter__(self):
        self._context = et.iterparse(self._filepath, events=("start", "end"))

        # get the root element
        event, self._root = next(self._context)
        return self

    def read(self) -> Generator[et.Element, None, None]:
        # get the root element
        for event, elem in self._context:
            if event == "end":
                yield elem
                self._root.clear()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._context = None


class AppleHealthDataReaderContextManager(XmlReaderContextManager):
    def __init__(self, filepath: str):
        super().__init__(filepath)

    def read(self):
        for event, elem in self._context:
            if event == "end":
                if elem.tag in hd.HEALTH_ROOT_CHILDREN:
                    yield elem

                self._root.clear()


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
            row['startDate'] = localize_apple_health_datetime_str(row['startDate'])
            row['endDate'] = localize_apple_health_datetime_str(row['endDate'])
            row['creationDate'] = localize_apple_health_datetime_str(row['creationDate'])

        self._writer.writerow(row)


class HKWorkoutXmlCsvDictWriter(HKXmlCsvDictWriterContextManager):
    _metadata_entry_fields = set(hd.Fieldnames_Workout_MetadataEntry)

    def __init__(self, filepath: str, fieldnames: List[str], use_local_time: bool = True):
        super().__init__(filepath, fieldnames)
        self._use_local_time = use_local_time

    def write_xml_elem(self, elem: et.Element):
        row = elem.attrib.copy()
        kv = {mde.attrib['key']: mde.attrib['value'] for mde in elem.findall('MetadataEntry')}

        for k in HKWorkoutXmlCsvDictWriter._metadata_entry_fields:
            row[k] = kv.get(k, '')

        if self._use_local_time:
            row['startDate'] = localize_apple_health_datetime_str(row['startDate'])
            row['endDate'] = localize_apple_health_datetime_str(row['endDate'])
            row['creationDate'] = localize_apple_health_datetime_str(row['creationDate'])

        self._writer.writerow(row)

