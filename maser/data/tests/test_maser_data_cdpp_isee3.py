import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data.cdpp import CDPPDataFromFile
from maser.data.cdpp.isee3.sbh import ISEE3SBHData, read_isee3_sbh_3d_radio_source

load_test_data("cdpp")


def load_isee3_sbh_3d_radio_source():
    file_path = get_data_directory() / "cdpp" / "isee3" / "SBH_ISEE3_19780820"
    return read_isee3_sbh_3d_radio_source(str(file_path))


class ISEE3SBHDataTest(unittest.TestCase):

    """Test case for ISEE3SBHData class"""

    def test_cdpp_data_class(self):
        header = {}
        data = {}
        meta = {}
        orbit = {}
        name = "TEST"
        test = ISEE3SBHData("", header, data, meta, name, orbit)
        self.assertIsInstance(test, CDPPDataFromFile)

    def test_isee3_sbh_3d_radio_source_name(self):
        print("### Testing ISEE3SBHData name variable on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        self.assertEqual(a.name, "ISEE3_SBH_3D_RADIO_SOURCE")

    def test_isee3_sbh_3d_radio_source_len(self):
        print("### Testing ISEE3SBHData len() method on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        self.assertEqual(len(a), 665)

    def test_isee3_sbh_3d_radio_source_keys(self):
        print("### Testing ISEE3SBHData keys() method on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        expected_set = {'CCSDS_PREAMBLE', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3", "CCSDS_B4", "CCSDS_B5",
                        "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", 'T_Field', 'P_Field',
                        'CALEND_YEAR', 'CALEND_MONTH', 'CALEND_DAY', 'CALEND_HOUR', 'CALEND_MINUTE', 'CALEND_SECOND',
                        'MILLI_SECOND', 'JULIAN_SECOND',
                        'N_S', 'TIME_QUALITY', 'SPACECRAFT_POSITION_Z', 'N_FREQ_STEP',
                        'CYCLE_NUMBER', 'S_SAMPLE_INTERVAL', 'N_MEAS_STEP',
                        'SPIN_PERIOD', 'SPACECRAFT_POSITION_Y',
                        'TM_FORMAT', 'N_FREQ_PER_MEAS_STEP',
                        'NUMBER_OF_OK_STEPS', 'S_ANTENNA',
                        'SUN_TIME', 'MINOR_FRAME_DURATION', 'DATA_RATE',
                        'SUN_S_ANTENNA_TIME', 'N_Z', 'RECEIVER_MODE',
                        'SPACECRAFT_POSITION_X', 'DSC_29', 'CYCLE_DURATION', 'N_PHI', 'DSC_28', 'DSC_27',
                        'STEP_DURATION', 'SUN_PERIOD', 'DATETIME', 'FREQUENCY', 'S_DATA', 'DATA_QUALITY',
                        'TIME', 'BANDWIDTH', 'PHI_DATA', 'Z_DATA'}
        keys_set = set(a.keys())
        self.assertSetEqual(keys_set, expected_set)

    def test_isee3_sbh_3d_radio_source_datetime(self):
        print("### Testing ISEE3SBHData \"DATETIME\" key on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1978, 8, 20, 0, 2, 18, 382000))


