import configparser

from emulator import Emulator


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    computer = config['Emulator']['computer']
    filename = config['Emulator']['filename']

    emulator = Emulator(computer, filename)
    emulator.execute()


if __name__ == "__main__":
    main()
