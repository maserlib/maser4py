import unittest
import os
from maser.data.data import *
from maser.data.tests import load_test_data, get_data_directory

load_test_data("cdpp")
file_path = get_data_directory() / "cdpp" / "isee3" / "SBH_ISEE3_19780820"


class MaserDataFromFileTest(unittest.TestCase):

    """Test case for MaserData class"""

    def test_file_name_method(self):
        o = MaserDataFromFile(str(file_path))
        self.assertEqual(o.get_file_name(), 'SBH_ISEE3_19780820')

    def test_file_path_method(self):
        o = MaserDataFromFile(str(file_path))
        self.assertEquals(o.get_file_path(), str(file_path.parent))

    def test_file_size_method(self):
        o = MaserDataFromFile(str(file_path))
        self.assertEquals(o.get_file_size(), 5817420)

