from .parser_base import ParserBase
from utils import normalize_date, JsonTools, integer_to_word, to_integer

FEATURES = {
    'SD2': 'seat in a quiet zone',
    'SD3': 'window',
    'SD5': 'aisle',
    'SD12': 'overwing',
    'SD14': 'exit',
    'SD15': 'leg space seat',
    'SD17': 'seat with facilities for handicapped',
    'SD18': 'seat with facilities for handicapped incapacitated passenger',
    'SD21': 'rear facing seat',
}


class SeatInfoParser(JsonTools):

    def __init__(self, row, offers):
        self.column = row.find('./').text
        self.offers = self.parse_offers(offers)
        self.seat_info = row.findall('./Seat')
        self.seat_list = []

    def parse_offers(self, offers):
        offer_data_path = './UnitPriceDetail/TotalAmount/SimpleCurrencyPrice'
        offer_data = {}
        for o in offers:
            offer_data[o.attrib['OfferItemID']] = {
                'fee': {
                    'amount': to_integer(o.find(offer_data_path).text.replace('.', '')),
                    'currency_code': o.find(offer_data_path).attrib['Code'].lower(),
                },
                'taxes': {
                    'amount': None,
                    'currency_code': None,
                }
            }
        return offer_data

    def parse(self):  # pragma: no cover
        for si in self.seat_info:
            seat = self.parse_id_and_availability(si)
            self.parse_features(si, seat)
            self.parse_service(si, seat)
            self.seat_list.append(seat)

    def parse_id_and_availability(self, si):
        occupied = 'SD19'
        return {
            'seat_id': f'{self.column}{si.find("./").text}',
            'occupied': occupied in [d.text for d in list(si)],
        }

    def parse_features(self, si, seat):
        seat['features'] = [FEATURES.get(i.text) for i in list(si) if FEATURES.get(i.text)]
        if 'window' not in seat['features'] and 'aisle' not in seat['features']:
            seat['features'].append('center')
        return seat

    def parse_service(self, si, seat):
        try:
            seat.update(self.offers.get(si.find('./OfferItemRefs').text))
        except AttributeError:
            seat.update({
                'fee': {'amount': None, 'currency_code': None},
                'taxes': {'amount': None, 'currency_code': None},
            })
        return seat


class SeatMapTwoToJson(ParserBase):

    def parse_flight_data(self):
        element = self.main_xml_element.find('./DataLists/FlightSegmentList/')
        self.json['flight'] = {
            'number': element.find('./MarketingCarrier/FlightNumber').text,
            'departure_airport': element.find('./Departure/AirportCode').text,
            'arrival_airport': element.find('./Arrival/AirportCode').text,
            'departure_date_time': normalize_date(
                f'{element.find("./Departure/Date").text}T{element.find("./Departure/Time").text}',
            ),
            'air_equip_type': element.find('./Equipment/AircraftCode').text,
        }

    def parse_seat_map(self):
        offers = list(self.main_xml_element.find('./ALaCarteOffer'))
        for seatmap in self.main_xml_element.findall('./SeatMap'):
            data = {
                'cabin_layout': self.parse_cabin_data(seatmap.find('./Cabin')),
                'cabin_type': None,
            }
            for row in seatmap.findall('./Cabin/Row'):
                sip = SeatInfoParser(row, offers)
                sip.parse()
                data[f'row_{integer_to_word(row.find("./").text)}'] = sip.seat_list
                self.json['seat_map'].append(data)

    def parse_cabin_data(self, cabin):
        pos = [col.attrib['Position'] for col in cabin.findall('./CabinLayout/Columns')]
        return f"{''.join(pos[:len(pos)//2])} {''.join(pos[len(pos)//2:])}"
