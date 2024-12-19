import toml
import subprocess
from typing import Dict, List

def parse_toml_config(config_path: str) -> Dict[str, str]:
    """Parses a TOML configuration file."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = toml.load(f)["config"]
        return config
    except FileNotFoundError as ex:
        print(f"Config file not found: {ex}")
    except toml.TomlDecodeError as ex:
        print(f"Error decoding TOML file: {ex}")
    return {}

def get_dependencies(package_name: str) -> List[str]:
    """Returns a list of dependencies for a given pip package."""
    result = subprocess.run(
        ["pip", "show", package_name], capture_output=True, text=True)

    if result.returncode != 0:
        raise ValueError(f"Error: Package '{package_name}' not found.")

    dependencies = []
    for line in result.stdout.splitlines():
        if line.startswith("Requires:"):
            dependencies = line.split(": ")[1].split(", ")

    dependencies = [dep.strip() for dep in dependencies if dep]
    return dependencies

def build_dependency_graph(package_name: str, max_depth: int = 5) -> List[str]:
    """Recursively build the dependency graph for the package using PlantUML format."""
    graph = []
    visited = set()

    def add_dependencies(pkg_name: str, current_depth: int):
        if current_depth > max_depth or pkg_name in visited:
            return
        visited.add(pkg_name)

        dependencies = get_dependencies(pkg_name)

        for dep in dependencies:
            graph.append(f"{pkg_name} --> {dep}")
            add_dependencies(dep, current_depth + 1)

    add_dependencies(package_name, 1)
    return graph

def generate_plantuml_script(graph: List[str]) -> str:
    """Generate a PlantUML script based on the dependency graph."""
    plantuml_script = "@startuml\n"
    for relation in graph:
        plantuml_script += f"{relation}\n"
    plantuml_script += "@enduml"
    return plantuml_script

def save_plantuml_script(script: str, output_path: str) -> None:
    """Save the PlantUML script to a file."""
    with open(output_path, "w") as f:
        f.write(script)

def visualize_graph(visualizer_path: str, script_path: str, image_path: str) -> None:
    """Visualize the graph using the specified PlantUML graph visualizer program."""
    try:
        subprocess.run(
            ["java", "-jar", visualizer_path, script_path, "-o", image_path], check=True
        )
    except subprocess.CalledProcessError as ex:
        print(f"Error running PlantUML: {ex}")

def main():
    config_path = "config.toml"
    config = parse_toml_config(config_path)

    if not config:
        print("Failed to load configuration.")
        return

    package_name = config["package_name"]
    visualizer_path = config["visualizer_path"]
    graph_image_path = config.get("graph_image_path", "dependency_graph.png")

    if not package_name or not visualizer_path:
        print("Configuration file is missing required fields.")
        return

    try:
        graph = build_dependency_graph(package_name)
    except ValueError as ex:
        print(ex)
        return

    script = generate_plantuml_script(graph)
    save_plantuml_script(script, "dependency_graph.puml")
    visualize_graph(visualizer_path, "dependency_graph.puml", graph_image_path)

if __name__ == "__main__":
    main()
