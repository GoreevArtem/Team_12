"""Module for testing configs"""

import unittest
import json
from config_bot import Config


class MyTestCase(unittest.TestCase):
    """Class for testing configs"""

    def setUp(self) -> None:
        self.config_file = '../config.json'

    def set_up_keys_as_str(self, d: dict):
        """Make keys to strings and nested dicts too"""
        l = []
        for key in d:
            if not isinstance(key, str) or isinstance(d[key], dict):
                l.append(key)

        for key in l:
            if isinstance(d[key], dict):
                d[key] = self.set_up_keys_as_str(d[key])
            else:
                d[str(key)] = d[key]
                del d[key]
        return d

    def test_config_json(self):
        """Function for testing configs"""
        data = {'first_param': 5, '1': '4', '3': 45, 'second_param': [1, 2, 3],
                't': {1: 1}}
        data = self.set_up_keys_as_str(data)
        with open(self.config_file, 'w+') as file:
            json.dump(data, file)
        config = Config()
        self.assertEqual(config.properties, data)
        if __name__ == '__main__':
            unittest.main()
