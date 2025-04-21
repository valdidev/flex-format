import yaml

def parse(yaml_str):
    """Valida y parsea YAML a diccionario Python"""
    return yaml.safe_load(yaml_str)

def convert(data):
    """Convierte datos Python a YAML formateado"""
    return yaml.dump(data, allow_unicode=True, sort_keys=False, indent=2)