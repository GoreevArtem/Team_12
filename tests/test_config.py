"""Module for testing configs"""

import unittest
import json
from config_bot import Config


class MyTestCase(unittest.TestCase):
    """Class for testing configs"""

    def setUp(self) -> None:
        self.config_file = "../config.json"

    def set_up_keys_as_str(self, test_dict: dict):
        """Make keys to strings and nested dicts too"""
        keys_list = []
        for key in test_dict:
            if not isinstance(key, str) or isinstance(test_dict[key], dict):
                keys_list.append(key)

        for key in keys_list:
            if isinstance(test_dict[key], dict):
                test_dict[key] = self.set_up_keys_as_str(test_dict[key])
            else:
                test_dict[str(key)] = test_dict[key]
                del test_dict[key]
        return test_dict

    def config_dict(self, test_dict: dict):
        """Test for a single dict"""
        data = self.set_up_keys_as_str(test_dict)
        with open(self.config_file, "w+", encoding="utf-8") as file:
            json.dump(data, file)
        config = Config()
        self.assertEqual(config.properties, data)
        Config._properties = None
        Config._instance = None

    def test_config_json(self):
        """Function for testing configs"""
        data = {
            "first_param": 5,
            "1": "4",
            "3": 45,
            "second_param": [1, 2, 3],
            "t": {1: 1},
        }
        self.config_dict(data)
        data = {1: [1, 2, ["first", "second", []]], "test": None, 4.56: 7.89}
        self.config_dict(data)


if __name__ == "__main__":
    unittest.main()
