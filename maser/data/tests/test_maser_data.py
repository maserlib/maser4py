import unittest
import os
from maser.data.data import *


class MaserDataFromFileTest(unittest.TestCase):

    """Test case for MaserData class"""

    def test_file_name_method(self):
        o = MaserDataFromFile('data/SBH_ISEE3_19780820')
        self.assertEqual(o.get_file_name(), 'SBH_ISEE3_19780820')

    def test_file_path_method(self):
        o = MaserDataFromFile('data/SBH_ISEE3_19780820')
        self.assertEquals(o.get_file_path(), os.path.join(os.path.abspath(os.path.curdir), 'data'))

    def test_file_size_method(self):
        o = MaserDataFromFile('data/SBH_ISEE3_19780820')
        self.assertEquals(o.get_file_size(), 5817420)

