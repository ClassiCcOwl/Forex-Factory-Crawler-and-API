import configparser


def getconfigs():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
