import sys
import requests


def get_time():
    url = "http://worldtimeapi.org/api/timezone/Europe/Moscow"
    resp = requests.get(url)
    return resp.json()['unixtime']


def print_time(unixtime):
    try:
        from get_pretty_time_package.pretty_print_module import print_time_pretty
        print_time_pretty(unixtime)
    except ImportError:
        print(unixtime)


"""    finally:
        print("Вывод времени в unix")"""


def main(*args, **kwargs):
    print_time(get_time())


if __name__ == "__main__":
    sys.exit(main() or 0)
