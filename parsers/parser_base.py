from utils import JsonTools

class ParserBase(JsonTools):
    encoding = 'UTF-8'
    json = {}
    json['seat_map'] = []

    def __init__(self, main_xml_element):
        self.main_xml_element = main_xml_element

    def parse(self):
        self.extract_flight_data()
        self.extract_seat_map()
