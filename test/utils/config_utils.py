import configparser
import pathlib


def local_browser():
    parser = configparser.ConfigParser()
    parser.read(pathlib.Path(__file__).parent.parent.absolute() / "config")
    return parser.getboolean('browser', 'local')
