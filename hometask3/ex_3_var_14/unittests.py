import unittest

from main import *

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.parser = ConfigParser()

    def test_handle_global_declaration(self):
        line = "global pi = 3.14"
        self.parser.handle_global_declaration(line)
        self.assertIn("pi", self.parser.constants)
        self.assertEqual(self.parser.constants["pi"], 3.14)

    def test_handle_assignment(self):
        line = "settings = [resolution: 1920x1080, fullscreen: true, volume: 75]"
        self.parser.handle_assignment(line)
        self.assertIn(("settings", {'resolution': '1920x1080', 'fullscreen': 'true', 'volume': '75'}),
                      self.parser.config_elements)

    def test_parse_dict(self):
        dict_str = "resolution: 1920x1080, fullscreen: true, volume: 75"
        result = self.parser.parse_dict(dict_str)
        self.assertEqual(result["resolution"], "1920x1080")
        self.assertEqual(result["fullscreen"], "true")
        self.assertEqual(result["volume"], "75")

    def test_to_xml(self):
        self.parser.constants = {"pi": 3.14, "max_value": 100}
        self.parser.global_elements = [("pi", 3.14), ("max_value", 100)]
        self.parser.config_elements = [("settings", {"resolution": "1920x1080", "fullscreen": "true", "volume": "75"})]
        xml_output = self.parser.to_xml()
        self.assertIn("<global name=\"pi\" value=\"3.14\"/>", xml_output)
        self.assertIn("<settings>", xml_output)

    def test_syntax_error_handling(self):
        line = "global pi = 3.14.14"  # Некорректная строка
        with self.assertRaises(SyntaxError):
            self.parser.handle_global_declaration(line)


if __name__ == "__main__":
    unittest.main()
