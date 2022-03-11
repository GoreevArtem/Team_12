"""Test for class Utils"""

import unittest
import os
from extra.utils import Utils


class TestUtils(unittest.TestCase):
    """Test for class Utils"""

    def test_clear_dir(self):
        """Test for clean_dir in Utils"""
        num_files = 10
        file_dir = "test_directory"
        for i in range(num_files):
            with open(f"{file_dir}/{i}.bin", "wb") as file:
                file.write(i.to_bytes(byteorder="little", length=8))
        self.assertEqual(len(os.listdir(file_dir)), num_files)
        Utils.clear_dir(file_dir)
        self.assertEqual(len(os.listdir(file_dir)), 0)


if __name__ == "__main__":
    unittest.main()
