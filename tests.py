import unittest
from xml.etree import ElementTree as Eltree
import pathlib
from utils import (
    get_cleaned_xml,
    normalize_date,
    JsonTools,
    to_boolean,
    to_integer,
    integer_to_word
)
from parsers.seatmap_one import SeatMapOneToJson, SeatInfoParser
from parsers.seatmap_two import SeatMapTwoToJson, SeatInfoParser as SIPTwo
from seatmap_parser import start_parser
import os

PROJECT_PATH = str(pathlib.Path().absolute())


class ToolsTestCase(unittest.TestCase):

    def setUp(self):
        self.filepath = f'{PROJECT_PATH}/seatmap1.xml'

    def test_string_must_be_converted_to_boolean_or_return_original_value(self):
        self.assertTrue(to_boolean('true'))
        self.assertEqual('test', to_boolean('test'))

    def test_string_must_be_converted_to_integer_or_return_original_value(self):
        self.assertEqual(1, to_integer('1'))
        self.assertEqual('test', to_integer('test'))

    def test_integer_must_return_as_string(self):
        self.assertEqual('one', integer_to_word(1))
        self.assertEqual('thirteen', integer_to_word(13))

    def test_namespaces_must_be_removed_from_string_xml(self):
        xml = Eltree.tostring(Eltree.parse(self.filepath).getroot(), encoding='UTF-8').decode('UTF-8')
        self.assertIn('ns:', xml)
        self.assertNotIn('ns:', get_cleaned_xml(self.filepath))

    def test_date_must_be_normalized(self):
        normalized_date = '2020-01-01T12:00:00'
        self.assertEqual(
            normalized_date,
            normalize_date('2020-01-01T12:00'),
        )

    def test_json_must_be_normalized(self):
        normalized_json = {'test': True, 'camel_case_key': True}
        self.assertEqual(normalized_json, JsonTools.normalize_json({'Test': True, 'CamelCaseKey': True}))

    def test_json_file_must_be_created_using_xml_filename(self):
        self.assertNotIn('seatmap1_parsed.json', os.listdir(PROJECT_PATH))
        jt = JsonTools({'test': True, 'camel_case_key': True})
        jt.export_json('seatmap1.xml')
        self.assertIn('seatmap1_parsed.json', os.listdir(PROJECT_PATH))
        os.remove(f'{PROJECT_PATH}/seatmap1_parsed.json')


class SeatMapOneTestCase(unittest.TestCase):

    def setUp(self):
        xml = get_cleaned_xml(f'{PROJECT_PATH}/seatmap1.xml')
        self.main_xml_element = xml.find(
            './Body/OTA_AirSeatMapRS/SeatMapResponses/SeatMapResponse',
        )
        self.smo = SeatMapOneToJson(self.main_xml_element)
        self.seat_info = self.main_xml_element.find('./SeatMapDetails/CabinClass/RowInfo/SeatInfo')
        self.sip = SeatInfoParser(None)

    def test_id_and_availability_must_be_parsed(self):
        self.assertEqual(
            {'seat_id': '1A', 'occupied': False},
            self.sip.parse_id_and_availability(self.seat_info),
        )

    def test_feature_data_must_be_parsed(self):
        self.assertEqual({'features': ['window']}, self.sip.parse_features(self.seat_info, {}))

    def test_service_data_must_return_with_none_values_if_no_service_data_in_seat_data(self):
        self.assertEqual(
            {'fee': {'amount': None, 'currency_code': None}, 'taxes': {'amount': None, 'currency_code': None}},
            self.sip.parse_service(self.seat_info, {}),
        )

    def test_service_data_must_return_when_service_data_on_seat(self):
        seat_info = '''
            <SeatInfo BlockedInd="false" BulkheadInd="false" ColumnNumber="3" ExitRowInd="false" GalleyInd="false" GridNumber="3" PlaneSection="Left">
                <Summary AvailableInd="true" InoperativeInd="false" OccupiedInd="false" SeatNumber="12C"/>
                <Features extension="Preferred">Other_</Features>
                <Features>Aisle</Features>
                <Features extension="Chargeable">Other_</Features>
                <Service CodeContext="Preferred">
                    <Fee Amount="4200" CurrencyCode="USD" DecimalPlaces="2">
                        <Taxes Amount="0" CurrencyCode="USD"/>
                    </Fee>
                </Service>
            </SeatInfo>
        '''
        self.assertEqual(
            {'fee': {'amount': 4200, 'currency_code': 'usd'}, 'taxes': {'amount': 0, 'currency_code': 'usd'}},
            self.sip.parse_service(Eltree.fromstring(seat_info), {}),
        )

    def test_flight_data_must_be_extracted(self):
        data = {
            'number': '1179',
            'departure_airport': 'LAS',
            'arrival_airport': 'IAH',
            'departure_date_time': '2020-11-22T15:30:00',
            'air_equip_type': '739'
        }
        self.assertNotEqual(data, self.smo.json.get('flight'))
        self.smo.parse_flight_data()
        self.assertEqual(data, self.smo.json.get('flight'))

    def test_seat_map_must_be_parsed(self):
        self.assertFalse(self.smo.json['seat_map'])
        self.smo.parse_seat_map()
        self.assertEqual(
            '1A',
            self.smo.json['seat_map'][0]['row_one'][0]['seat_id'],
        )


class SeatMapTwoTestCase(unittest.TestCase):

    def setUp(self):
        self.xml = get_cleaned_xml(f'{PROJECT_PATH}/seatmap2.xml')
        self.offers = list(self.xml.find('./ALaCarteOffer'))
        self.row = self.xml.find('./SeatMap/Cabin/Row')
        self.seat_info = self.row.find('./Seat')
        self.sip = SIPTwo(self.row, self.offers)
        self.simple_seat_info = Eltree.fromstring(
            '''
                <Seat>
                    <Column>A</Column>
                </Seat>
            '''
        )
        self.smt = SeatMapTwoToJson(self.xml)

    def test_offer_data_must_be_parsed(self):
        parsed_offers = {
            "OFIa20ae42f-6417-11eb-b326-15132ca0c3351": {
                "fee": {"amount": 2210, "currency_code": "gbp"},
                "taxes": {"amount": None, "currency_code": None},
            },
            "OFIa20ae42f-6417-11eb-b326-15132ca0c3352": {
                "fee": {"amount": 3540, "currency_code": "gbp"},
                "taxes": {"amount": None, "currency_code": None},
            },
            "OFIa20ae42f-6417-11eb-b326-15132ca0c3353": {
                "fee": {"amount": 1770, "currency_code": "gbp"},
                "taxes": {"amount": None, "currency_code": None},
            },
            "OFIa20ae42f-6417-11eb-b326-15132ca0c3354": {
                "fee": {"amount": 1150, "currency_code": "gbp"},
                "taxes": {"amount": None, "currency_code": None},
            },
        }
        self.assertEqual(parsed_offers, self.sip.offers)

    def test_id_and_availability_must_be_parsed(self):
        self.assertEqual(
            {'seat_id': '7A', 'occupied': False},
            self.sip.parse_id_and_availability(self.seat_info),
        )

    def test_feature_data_must_be_parsed(self):
        self.assertEqual(
            {'features': ['seat in a quiet zone', 'window']},
            self.sip.parse_features(self.seat_info, {}),
        )

    def test_seat_must_receive_center_if_no_aisle_or_window_on_features(self):
        self.assertEqual(
            {'features': ['center']},
            self.sip.parse_features(self.simple_seat_info, {}),
        )

    def test_payment_data_must_be_parsed_from_seat(self):
        self.assertEqual(
            {
                'fee': {'amount': None, 'currency_code': None},
                'taxes': {'amount': None, 'currency_code': None},
            },
            self.sip.parse_service(self.simple_seat_info, {}),
        )

    def test_payment_data_return_with_no_values_if_no_payment_element_in_seat_info(self):
        seat_info = Eltree.fromstring('''
            <Seat>
                <Column>A</Column>
            </Seat>
        '''
        )
        self.assertEqual(
            {
                'fee': {'amount': 2210, 'currency_code': 'gbp'},
                'taxes': {'amount': None, 'currency_code': None},
            },
            self.sip.parse_service(self.seat_info, {}),
        )

    def test_flight_data_must_be_extracted(self):
        data = {
            'number': '1415',
            'departure_airport': 'FNC',
            'arrival_airport': 'DUS',
            'departure_date_time': '2021-08-26T17:45:00',
            'air_equip_type': '320',
        }
        self.assertNotEqual(data, self.smt.json.get('flight'))
        self.smt.parse_flight_data()
        self.assertEqual(data, self.smt.json.get('flight'))

    def test_seat_map_must_be_parsed(self):
        self.smt.json['seat_map'] = []
        self.assertFalse(self.smt.json['seat_map'])
        self.smt.parse_seat_map()
        self.assertEqual(
            '7A',
            self.smt.json['seat_map'][0]['row_seven'][0]['seat_id'],
        )

    def tearDown(self):
        self.smt = None

if __name__ == '__main__':
    unittest.main()
