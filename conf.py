import configparser

conf = configparser.ConfigParser()


def init_conf():
    conf.read('conf.ini')


if __name__ == '__main__':
    init_conf()
