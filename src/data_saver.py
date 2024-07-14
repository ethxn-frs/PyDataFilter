import pandas as pd
import json
import yaml
import xml.etree.ElementTree as ET

def save_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def save_xml(data, file_path):
    root = ET.Element("root")
    for item in data:
        elem = ET.Element("item")
        for key, val in item.items():
            child = ET.Element(key)
            if isinstance(val, list):
                child.text = ','.join(map(str, val))
            else:
                child.text = str(val)
            elem.append(child)
        root.append(elem)

    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
