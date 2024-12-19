# Python Package Dependency Graph Visualizer

Визуализация зависимостей пакетов Python, включая транзитивные зависимости, с использованием PlantUML

## Возможности 

* Рекурсивно исследует зависимости пакетов с з
аданной глубиной.
* Создает скрипт PlantUML, представляющий график зависимостей.
* Сохраняет изображение графика зависимостей в заданном местоположении.
* Поддерживает визуализацию с использованием заданного пользователем файла PlantUML jar.
* Настройка с помощью файла TOML.
* Поддерживает Python 3.7+
  
## Требования

* Python 3.7 или более поздней версии
* `pip` установлен и доступен в вашем PATH.
* JAR-файл PlantUML (например, `plantuml.jar`). Вы можете загрузить его с [веб-сайта PlantUML](http://plantuml.com/download).
* Java установлена и доступна в вашем PATH (требуется для запуска PlantUML jar).

## Скачивание

1. Клонировать этот репозиторий:
    ```bash
    git clone https://github.com/wilex-cr/pip_dependency_visualizer.git
    ```
2. Перейдите в каталог проекта:
    ```bash
    cd pip_dependency_visualizer
    ```
3. Установите необходимые пакеты Python:
    ```bash
    pip install -r requirements.txt
    ```

## Настройка

Создайте файл `config.toml` в корневом каталоге проекта со следующей структурой:

```toml
[config]
package_name = "your-package-name"  # Replace with the package you want to visualize
visualizer_path = "path/to/plantuml.jar" # Replace with the path to your PlantUML jar file
repository_url = "url-to-repository"
graph_image_path = "dependency_graph.png"  # Path to the output graph image
```

Замените ""your-package-name"" на имя пакета pip, который вы хотите проанализировать, ""path/to/plantuml.jar"" - на фактический путь к вашему jar-файлу PlantUML, а ""dependency_graph.png"" - на желаемый путь к выходному изображению.

## Использование

Запуск приложения:

```bash
python .\src\dependency_visualizer.py
```

Это приведет к созданию файла dependency_graph.pom и файла изображения (например, dependency_graph.png) в указанном расположении.

## Пример

Чтобы наглядно представить зависимости пакета "запросы", обновите свой файл "config.toml" следующим образом:

```toml
[config]
visualizer_path = ".\\plantuml-1.2024.7.jar"
package_name = "requests"
repository_url = "https://github.com/psf/requests"
graph_image_path = "requests_dependencies.png"
```

### Пример работы программы

![image](https://github.com/wilex-cr/Configuration/blob/main/hometask2/pip_dependency_visualizer-main/pip_dependency_visualizer-main/run_program2.png)

