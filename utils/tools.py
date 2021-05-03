from xml.etree import ElementTree
from re import sub
from json import dumps
from datetime import datetime


def to_boolean(value):
    if value in ['true', 'false']:
        return value == 'true'
    return value


def to_integer(value):
    try:
        return int(value)
    except ValueError:
        return value


def integer_to_word(number):
    return {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',
        21: 'twenty_one',
        22: 'twenty_two',
        23: 'twenty_three',
        24: 'twenty_four',
        25: 'twenty_five',
        26: 'twenty_six',
        27: 'twenty_seven',
        28: 'twenty_eight',
        29: 'twenty_nine',
        30: 'thirty',
    }.get(to_integer(number))


def get_cleaned_xml(filepath):
    xml = ElementTree.tostring(ElementTree.parse(filepath).getroot(), encoding='UTF-8').decode('UTF-8')
    return ElementTree.fromstring(sub(r'<(ns\d*?:)', '<', sub(r'<(\/ns\d*?:)', '</', xml)))


def normalize_string(value):
    return sub(r'(?<!^)(?=[A-Z])', '_', value).lower()


def normalize_date(date):
    date = datetime(
        *[int(i) for i in date.replace('T', '-').replace(':', '-').split('-')],
    )
    return date.isoformat()


class JsonTools:

    def __init__(self, json):
        self.json = json

    def export_json(self, filename):
        filename, extension = filename.split('.')
        with open(f'{filename}_parsed.json', 'w') as json_file:
            json_file.write(str(dumps(self.json, indent=2)))

    @staticmethod
    def normalize_json(json):
        new_json = {}
        for k, v in json.items():
            v = to_boolean(
                to_integer(v.lower()),
            ) if isinstance(v, str) else v
            new_json[normalize_string(k)] = v
        return new_json
