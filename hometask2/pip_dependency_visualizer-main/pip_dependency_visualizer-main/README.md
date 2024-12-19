# Python Package Dependency Graph Visualizer

Visualizing Python package dependencies, including transitive dependencies, using PlantUML

## Features

* Recursively explores package dependencies up to a configurable depth.
* Generates a PlantUML script representing the dependency graph.
* Saves the dependency graph image in a configurable location.
* Supports visualization using a user-specified PlantUML jar file.
* Configuration via a TOML file.
* Supports Python 3.7+

## Prerequisites

*   Python 3.7 or later
*   `pip` installed and accessible in your PATH.
*   PlantUML jar file (e.g., `plantuml.jar`). You can download it from the [PlantUML website](https://plantuml.com/download).
*   Java installed and accessible in your PATH (required to run the PlantUML jar).

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/wilex/pip_dependency_visualizer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd pip_dependency_visualizer
    ```
3. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `config.toml` file in the project root directory with the following structure:

```toml
[config]
package_name = "your-package-name"  # Replace with the package you want to visualize
visualizer_path = "path/to/plantuml.jar" # Replace with the path to your PlantUML jar file
repository_url = "url-to-repository"
graph_image_path = "dependency_graph.png"  # Path to the output graph image
```

Replace `"your-package-name"` with the name of the pip package you want to analyze, `"path/to/plantuml.jar"` with the actual path to your PlantUML jar file, and `"dependency_graph.png"` with the desired output image path.

## Usage

Run the script:

```bash
python .\src\dependency_visualizer.py
```

This will generate a `dependency_graph.puml` file and an image file (e.g., `dependency_graph.png`) in the specified location.

## Example

To visualize the dependencies of the `requests` package, update your `config.toml` as follows:

```toml
[config]
visualizer_path = ".\\plantuml-1.2024.7.jar"
package_name = "requests"
repository_url = "https://github.com/psf/requests"
graph_image_path = "requests_dependencies.png"
```
