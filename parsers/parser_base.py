from utils import JsonTools

class ParserBase(JsonTools):
    encoding = 'UTF-8'
    json = {}
    json['seat_map'] = []

    def __init__(self, main_xml_element):
        self.main_xml_element = main_xml_element

    def parse(self):  # pragma: no cover
        self.parse_flight_data()
        self.parse_seat_map()
