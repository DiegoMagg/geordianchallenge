import pathlib
from sys import argv
from utils import get_cleaned_xml
from parsers import SeatMapOneToJson, SeatMapTwoToJson


def start_parser(filename): # pragma: no cover
    seatmap_one_main_element = './Body/OTA_AirSeatMapRS/SeatMapResponses/SeatMapResponse'
    xml = get_cleaned_xml(f'{str(pathlib.Path().absolute())}/{filename}')
    if xml.find(seatmap_one_main_element):
        smo = SeatMapOneToJson(xml.find(seatmap_one_main_element))
    else:
        smo = SeatMapTwoToJson(xml)
    smo.parse()
    smo.export_json(filename)



if __name__ == '__main__':  # pragma: no cover
    start_parser(argv[-1])
