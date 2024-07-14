import pandas as pd
import json
import yaml


def load_csv(file_path):
    return pd.read_csv(file_path).to_dict(orient='records')


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def load_xml(file_path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []
    for elem in root:
        item = {}
        for subelem in elem:
            # Convert lists represented as strings to actual lists
            if ',' in subelem.text:
                item[subelem.tag] = list(map(int, subelem.text.split(',')))
            else:
                item[subelem.tag] = subelem.text if not subelem.text.isdigit() else int(subelem.text)
        data.append(item)
    return data