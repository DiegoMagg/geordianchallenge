from utils import JsonTools
from utils.tools import to_boolean, integer_to_word
from .parser_base import ParserBase


class SeatInfoParser(JsonTools):

    def __init__(self, seat_info):
        self.seat_info = seat_info
        self.seat_list= []

    def parse(self):
        for si in self.seat_info:
            seat = self.parse_id_and_availability(si)
            self.parse_features(si, seat)
            self.parse_service(si, seat)
            self.seat_list.append(seat)

    def parse_id_and_availability(self, si):
        return {
            'seat_id': si.find('./Summary').attrib['SeatNumber'],
            'occupied': to_boolean(si.find('./Summary').attrib['OccupiedInd']),
        }

    def parse_features(self, si, seat):
        seat['features'] = []
        feature_list = ['aisle', 'center', 'window', 'overwing', 'blockedseat permanent']
        for feature in si.findall('./Features'):
            if not feature.attrib and str(feature.text).lower() in feature_list:
                seat['features'].append(feature.text.lower().replace('_', ' '))
        return seat

    def parse_service(self, si, seat):
        seat.update({
            'fee': {'amount': None, 'currency_code': None},
            'taxes': {'amount': None, 'currency_code': None},
        })
        if si.find('./Service/Fee'):
            seat['fee'].update(self.normalize_json(dict(list(si.find('./Service/Fee').attrib.items())[:2])))
            seat['taxes'] = self.normalize_json(list(si.find('./Service/Fee'))[0].attrib)
        return seat


    def parse_additional_info(self, si):
        self.seat['additional_info'] = self.normalize_json(si.attrib)


class SeatMapOneToJson(ParserBase):

    def extract_flight_data(self):
        element = self.main_xml_element.find('./FlightSegmentInfo')
        self.json['flight'] = {
            'number': element.attrib['FlightNumber'],
            'departure_airport': element.find('./DepartureAirport').attrib['LocationCode'],
            'arrival_airport': element.find('./ArrivalAirport').attrib['LocationCode'],
            'departure_date_time': element.attrib['DepartureDateTime'],
            'air_equip_type': element.find('./Equipment').attrib['AirEquipType'],
        }

    def extract_seat_map(self):
        for cabin_class in list(self.main_xml_element.find('./SeatMapDetails')):
            data = {'cabin_layout': cabin_class.attrib['Layout']}
            for row_info in cabin_class.findall('./RowInfo'):
                data['cabin_type'] = row_info.attrib['CabinType'].lower()
                sip = SeatInfoParser(row_info.findall('./SeatInfo'))
                sip.parse()
                data[f"row_{integer_to_word(row_info.attrib['RowNumber'])}"] = sip.seat_list
                self.json['seat_map'].append(data)
