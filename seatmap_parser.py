from xml.etree import ElementTree
import pathlib
from sys import argv
from re import sub
from utils import get_cleaned_xml, make_json_keys_snake_case


class XMLToJson:
    encoding = 'UTF-8'
    json = {}

    def __init__(self, filename):
        self.xml = get_cleaned_xml(f'{str(pathlib.Path().absolute())}/{filename}')

    def parse(self):
        self.extract_flight_data()

    def extract_flight_data(self):
        element = self.xml.find('./Body/OTA_AirSeatMapRS/SeatMapResponses/SeatMapResponse/FlightSegmentInfo')
        self.json['flight'] = {
            'number': element.attrib['FlightNumber'],
            'departure_airport': element.find('./DepartureAirport').attrib['LocationCode'],
            'arrival_airport': element.find('./ArrivalAirport').attrib['LocationCode'],
            'departure_date_time': element.attrib['DepartureDateTime'],
            'air_equip_type': element.find('./Equipment').attrib['AirEquipType'],
        }


if __name__ == '__main__':  # pragma: no cover
    xmltojson = XMLToJson(argv[-1])
    xmltojson.parse()
