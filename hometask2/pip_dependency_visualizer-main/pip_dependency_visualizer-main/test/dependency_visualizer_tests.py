import unittest
import os

from src.dependency_visualizer import *


class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.config = parse_toml_config("config.toml")
        self.graph = build_dependency_graph(self.config["package_name"])
        self.script = generate_plantuml_script(self.graph)

    def test_parse_toml_config(self):
        self.assertEqual(
            self.config["visualizer_path"], ".\\plantuml-1.2024.7.jar")
        self.assertEqual(self.config["package_name"], "requests")
        self.assertEqual(self.config["repository_url"],
                         "https://github.com/psf/requests")

    def test_get_dependencies(self):
        dependencies = get_dependencies(self.config["package_name"])
        self.assertEqual(['certifi', 'charset-normalizer',
                         'idna', 'urllib3'], dependencies)

    def test_build_dependency_graph(self):
        self.assertEqual(['requests --> certifi', 'requests --> charset-normalizer',
                         'requests --> idna', 'requests --> urllib3'], self.graph)

    def test_generate_plantuml_script(self):
        self.assertEqual(
            "@startuml\nrequests --> certifi\nrequests --> charset-normalizer\nrequests --> idna\nrequests --> urllib3\n@enduml", self.script)

    def test_save_plantuml_script(self):
        save_plantuml_script(self.script, "test.puml")

        with open("test.puml", "r") as f:
            self.assertEqual(
                "@startuml\nrequests --> certifi\nrequests --> charset-normalizer\nrequests --> idna\nrequests --> urllib3\n@enduml", f.read())

        try:
            os.remove("test.puml")
        except:
            pass

    def test_visualize_graph(self):
        visualizer_path = ".\\plantuml-1.2024.7.jar"
        script_path = "test.puml"
        output_path = "test.png"

        save_plantuml_script(self.script, "test.puml")

        try:
            visualize_graph(visualizer_path, script_path)
            self.assertTrue(os.path.exists(output_path))
        finally:
            try:
                os.remove("test.puml")
                os.remove("test.png")
            except:
                pass
