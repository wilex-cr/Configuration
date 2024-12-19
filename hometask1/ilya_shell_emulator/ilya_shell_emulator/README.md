# UnixShellEmulator
 
Этот проект предоставляет базовый эмулятор оболочки Unix, который работает с архивом tar как с виртуальной файловой системой.

## Возможности

* Эмулирует основные команды Unix: `ls`, `cd`, `pwd`, `exit`, `history`.
* Работает с архивом tar без распаковки.
* Настраиваемое имя пользователя и название компьютера в командной строке.
* Запись команд в журнал с указанием временных меток и имени пользователя.
* Поддержка выполнения сценария запуска.

## Использование

Чтобы запустить эмулятор, используйте следующую команду:

```bash
python emulator.py -u [username] -c [computername] [filesystem.tar] -l [logfile.csv] -s [script.txt]
```

*  `-u, --user`:  Username (default: user)
*  `-c, --computer`: Computer name (default: localhost)
*  `<filesystem.tar>`: **Required**. Path to the tar archive containing the virtual filesystem.
*  `-l, --log`: Path to the log file (default: log.csv).
*  `-s, --script`: Path to a script file to execute on startup.

**Example:**

```bash
python emulator.py -u myuser -c mycomputer myfilesystem.tar -l mylog.csv -s myscript.txt 
```

## Использование Docker

Вы можете легко запустить эмулятор оболочки Unix с помощью Docker. Это позволяет создать согласованную среду без необходимости устанавливать зависимости на вашем локальном компьютере.

### Необходимые компоненты

- Установите Docker в свою систему. Следуйте инструкциям в разделе [Установка Docker].(https://docs.docker.com/get-docker/).

### Создайте образ Docker

Перейдите в каталог проекта, в котором находится ваш `Dockerfile` находится, и создайте образ Docker с помощью следующей команды:

```bash
docker build -t unixshell-emulator .
```

### Запуск программы

Чтобы запустить эмулятор, вы можете подключить локальный каталог, содержащий ваш архив tar и файл журнала. Используйте следующую команду:

```bash
docker run -it --rm -v /path/to/local/directory:/app/data unixshell-emulator /app/data/filesystem.tar -u [username] -c [computername] -l /app/data/logfile.csv -s /app/data/script.txt
```

### Пример работы программы

![image](https://github.com/wilex-cr/Configuration/blob/main/hometask1/ilya_shell_emulator/ilya_shell_emulator/run_program.jpg)

### Пример работы тестов

![image](https://github.com/wilex-cr/Configuration/blob/main/hometask1/ilya_shell_emulator/ilya_shell_emulator/run_tests.jpg)
