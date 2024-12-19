import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.global_elements = []
        self.config_elements = []

    def parse(self, input_text):
        lines = input_text.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("global"):
                self.handle_global_declaration(line)
            elif line:
                self.handle_assignment(line)

    def handle_global_declaration(self, line):
        match = re.match(r"global\s+([a-z][a-z0-9_]*)\s*=\s*(.*)", line)
        if match:
            name = match.group(1)
            value = match.group(2).strip()

            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                raise SyntaxError(f"Invalid value for global declaration: {value}")

            self.constants[name] = value
            self.global_elements.append((name, value))
        else:
            raise SyntaxError(f"Invalid global declaration syntax: {line}")

    def handle_assignment(self, line):
        match = re.match(r"([a-z][a-z0-9_]*)\s*=\s*(.*)", line)
        if match:
            name = match.group(1)
            value = match.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                value = self.parse_dict(value[1:-1].strip())
            elif value.startswith("$(+") and value.endswith(")"):
                value = self.constants.get(value[2:-1].strip())
            self.config_elements.append((name, value))
        else:
            raise SyntaxError(f"Invalid assignment: {line}")

    def parse_dict(self, dict_str):
        items = dict_str.split(",")
        parsed_items = {}
        for item in items:
            key, value = item.split(":")
            parsed_items[key.strip()] = value.strip()
        return parsed_items

    def to_xml(self):
        root = ET.Element("config")

        for global_name, global_value in self.global_elements:
            global_element = ET.SubElement(root, "global", name=global_name, value=str(global_value))

        for config_name, config_value in self.config_elements:
            config_element = ET.SubElement(root, "config", name=config_name)
            if isinstance(config_value, dict):
                settings_element = ET.SubElement(config_element, "settings")
                for key, value in config_value.items():
                    setting = ET.SubElement(settings_element, key)
                    setting.text = str(value)
            else:
                config_element.text = str(config_value)

        xml_str = ET.tostring(root, encoding="unicode", method="xml")
        parsed_xml = minidom.parseString(xml_str)
        return parsed_xml.toprettyxml(indent="  ")


def main(input_file, output_file):
    with open(input_file, 'r') as f:
        input_text = f.read()

    parser = ConfigParser()
    try:
        parser.parse(input_text)
        xml_output = parser.to_xml()
        with open(output_file, 'w') as out_f:
            out_f.write(xml_output)
    except SyntaxError as e:
        print(f"Syntax error: {e}")

if __name__ == "__main__":
    input_file = "config.txt"
    output_file = "output.xml"
    main(input_file, output_file)
