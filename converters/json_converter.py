import json

def parse(json_str):
    """Valida y parsea JSON a diccionario Python"""
    return json.loads(json_str)

def convert(data):
    """Convierte datos Python a JSON formateado"""
    return json.dumps(data, indent=2, ensure_ascii=False)