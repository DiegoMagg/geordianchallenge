from xml.etree import ElementTree
from re import sub


def make_json_keys_snake_case(json):
    new_json = {}
    for k, v in json.items():
        new_json[sub(r'(?<!^)(?=[A-Z])', '_', k).lower()] = v
    return new_json


def get_cleaned_xml(filepath):
    xml = ElementTree.tostring(ElementTree.parse(filepath).getroot(), encoding='UTF-8').decode('UTF-8')
    return ElementTree.fromstring(sub(r'<(ns\d*?:)', '<', sub(r'<(\/ns\d*?:)', '</', xml)))
