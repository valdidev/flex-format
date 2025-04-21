import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def parse(xml_str):
    """Valida y parsea XML a diccionario Python"""
    root = ET.fromstring(xml_str)
    return xml_to_dict(root)

def convert(data):
    """Convierte datos Python a XML formateado"""
    root = dict_to_xml(data)
    rough_string = ET.tostring(root, encoding="unicode")
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")

def xml_to_dict(element):
    """Convierte ElementTree XML a diccionario Python"""
    result = {}
    if element.tag:
        result[element.tag] = {}
        if element.text and element.text.strip():
            result[element.tag]["text"] = element.text.strip()
        for child in element:
            child_data = xml_to_dict(child)
            if child.tag in result[element.tag]:
                if isinstance(result[element.tag][child.tag], list):
                    result[element.tag][child.tag].append(child_data[child.tag])
                else:
                    result[element.tag][child.tag] = [result[element.tag][child.tag], child_data[child.tag]]
            else:
                result[element.tag].update(child_data)
    return result

def dict_to_xml(data, root_name="root"):
    """Convierte diccionario Python a ElementTree XML"""
    root = ET.Element(root_name)
    _dict_to_xml(data, root)
    return root

def _dict_to_xml(data, parent):
    for key, value in data.items():
        if isinstance(value, dict):
            child = ET.SubElement(parent, key)
            _dict_to_xml(value, child)
        elif isinstance(value, list):
            for item in value:
                child = ET.SubElement(parent, key)
                if isinstance(item, dict):
                    _dict_to_xml(item, child)
                else:
                    child.text = str(item)
        else:
            child = ET.SubElement(parent, key)
            child.text = str(value)