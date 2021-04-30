import unittest
from conf import settings
from seatmap_parser import XMLToJson
from xml.etree import ElementTree as Eltree
import pathlib
from utils import get_cleaned_xml


class ToolsTestCase(unittest.TestCase):

    def setUp(self):
        self.filepath = f'{str(pathlib.Path().absolute())}/seatmap1.xml'

    def test_namespaces_must_be_removed_from_string_xml(self):
        xml = Eltree.tostring(Eltree.parse(self.filepath).getroot(), encoding='UTF-8').decode('UTF-8')
        self.assertIn('ns:', xml)
        self.assertNotIn('ns:', get_cleaned_xml(self.filepath))


class XMLToJsonTestCase(unittest.TestCase):

    def setUp(self):
        self.xmltojson = XMLToJson('seatmap1.xml')
        self.flight_data = {
            'flight': {
                'number': '1179',
                'departure_airport': 'LAS',
                'arrival_airport': 'IAH',
                'departure_date_time': '2020-11-22T15:30:00',
                'air_equip_type': '739',
            },
        }

    def test_all_flight_data_must_be_extracted(self):
        data = {}
        self.assertFalse(self.xmltojson.json)
        data.update(self.flight_data)
        self.xmltojson.parse()
        self.assertEqual(data, self.xmltojson.json)

    def test_flight_data_must_be_extracted(self):
        self.xmltojson.json = {}
        self.assertEqual({}, self.xmltojson.json)
        self.xmltojson.extract_flight_data()
        self.assertEqual(self.xmltojson.json, self.flight_data)

    def tearDown(self):
        self.xmltojson.json = {}


if __name__ == '__main__':
    unittest.main()
