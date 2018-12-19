import unittest
from maser.data.cdpp import CDPPDataFromFile


class CDPPDataTest(unittest.TestCase):
    """Test case for CDPPData class"""

    def test_cdpp_data_class(self):
        print("### Testing CDPPData class")
        header = {}
        data = {}
        test = CDPPDataFromFile("", header, data, "")
        self.assertIsInstance(test, CDPPDataFromFile)
