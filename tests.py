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
        self.cabin_data = {
            'seats': [
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 1,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 1,
                        'plane_section': 'left',
                    },
                    'id': '1A',
                    'occupied': False,
                    'located_at': 'window',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 2,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 2,
                        'plane_section': 'left',
                    },
                    'id': '1B',
                    'occupied': False,
                    'located_at': 'aisle',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 4,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 4,
                        'plane_section': 'right',
                    },
                    'id': '1E',
                    'occupied': False,
                    'located_at': 'aisle',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 5,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 5,
                        'plane_section': 'right',
                    },
                    'id': '1F',
                    'occupied': False,
                    'located_at': 'window',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 1,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 1,
                        'plane_section': 'left',
                    },
                    'id': '2A',
                    'occupied': False,
                    'located_at': 'window',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 2,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 2,
                        'plane_section': 'left',
                    },
                    'id': '2B',
                    'occupied': False,
                    'located_at': 'aisle',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 4,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 4,
                        'plane_section': 'right',
                    },
                    'id': '2E',
                    'occupied': False,
                    'located_at': 'aisle',
                },
                {
                    'info': {
                        'blocked_ind': False,
                        'bulkhead_ind': False,
                        'column_number': 5,
                        'exit_row_ind': False,
                        'galley_ind': False,
                        'grid_number': 5,
                        'plane_section': 'right',
                    },
                    'id': '2F',
                    'occupied': False,
                    'located_at': 'window',
                },
            ],
            'cabin_layout': 'AB EF',
            'cabin_row': '2',
        },
        self.cabin_data = [
            {
                'cabin_layout': 'AB CD',
                'seats': [
                    {'row': 1, 'id': '1A'},
                ]
            },
        ]

    # def test_all_flight_data_must_be_extracted(self):
    #     data = {}
    #     self.assertFalse(self.xmltojson.json)
    #     data.update(self.flight_data)
    #     self.xmltojson.parse()
    #     self.assertEqual(data, self.xmltojson.json)

    # def test_flight_data_must_be_extracted(self):
    #     self.xmltojson.json = {}
    #     self.assertEqual({}, self.xmltojson.json)
    #     self.xmltojson.extract_flight_data()
    #     self.assertEqual(self.xmltojson.json, self.flight_data)

    def test_cabin_data_must_be_extracted(self):
        self.xmltojson.json = {}
        self.assertEqual({}, self.xmltojson.json)
        self.xmltojson.extract_cabin_data()
        breakpoint()
        self.assertEqual(self.xmltojson.json, self.flight_data)

    def tearDown(self):
        self.xmltojson.json = {}


if __name__ == '__main__':
    unittest.main()
