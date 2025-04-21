from converters import json_converter, xml_converter, yaml_converter

def validate_input(input_text, input_format):
    if not input_text:
        return {"text": "∅ Entrada vacía", "color": "#1e90ff"}, False

    try:
        if input_format == "JSON":
            json_converter.parse(input_text)
            return {"text": "✓ JSON válido", "color": "#32cd32"}, True
        elif input_format == "XML":
            xml_converter.parse(input_text)
            return {"text": "✓ XML válido", "color": "#32cd32"}, True
        elif input_format == "YAML":
            yaml_converter.parse(input_text)
            return {"text": "✓ YAML válido", "color": "#32cd32"}, True
    except Exception as e:
        return {"text": f"✗ Formato inválido ({str(e)})", "color": "#ff4040"}, False