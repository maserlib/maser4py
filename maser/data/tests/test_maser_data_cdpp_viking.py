import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data.cdpp import CDPPDataFromFile
from maser.data.cdpp.viking.v4n import VikingV4nData, read_viking

load_test_data("cdpp")


def load_viking_v4():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path))


def load_viking_v4_v1():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4_V1")


def load_viking_v4_v2():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4_V2")


def load_viking_v4l_fbl():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_FBL")


def load_viking_v4l_ni():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_Ni")


def load_viking_v4l_dft():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_DFT")


def load_viking_v4l_wf():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_WF")


def load_viking_v4h_sfa():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4H_SFA")


def load_viking_v4h_fb():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4H_FB")


class VikingV4nDataTest(unittest.TestCase):

    """Test case for VikingV4nData class"""
    def test_cdpp_data_class(self):
        header1 = {}
        header2 = {}
        header3 = {}
        data = {}
        meta = {}
        status = {}
        orbit = {}
        name = "TEST"
        test = VikingV4nData("", header1, header2, header3, status, data, name, meta, orbit)
        self.assertIsInstance(test, CDPPDataFromFile)

    """VIKING_V4"""

    def test_viking_v4_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4 dataset")
        a = load_viking_v4()
        self.assertEqual(a.name, "VIKING_V4")

    def test_viking_v4_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4 dataset")
        a = load_viking_v4()
        self.assertEqual(len(a), 12)

    def test_viking_v4_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4 dataset")
        a = load_viking_v4()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8", 'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE',
                        'NUMBER_OF_SERIES_IN_CURRENT_SWEEP', 'UTC_CALENDAR_DAY',
                        'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD', 'TM_LACK_BEFORE_SWEEP',
                        'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP', 'CALENDER_MONTH',
                        'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND',
                        'UTC_CALENDAR_HOUR', 'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER',
                        'CALENDAR_SECOND', 'UTC_CALENDER_MONTH', 'DATETIME', 'FREQUENCY_FB', 'ELECTRIC_FB',
                        'MAGNETIC_FB', 'V2_THETA', 'V2_AMPLITUDE', 'V2_PHI', 'V2_PSI', 'FREQUENCY_FBL',
                        'ELECTRIC_FBL', 'MAGNETIC_SFA', 'ELECTRIC_SFA', 'FREQUENCY_SFA', 'V1_ED', 'V1_EPDIFF',
                        'V1_EPAR', 'V1_EC', 'V1_VFG', 'V1_ID', 'V1_IFILL', 'V1_USER_BIAS', 'V1_RELATIVE_TIME',
                        'V1_VGUARD', 'DFT', 'N2_PROBE', 'N1_PROBE', 'WF1', 'WF2',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }
        key_set = set(a.keys())
        self.assertSetEqual(key_set, expected_set)

    def test_viking_v4_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4 dataset")
        a = load_viking_v4()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4_V1"""

    def test_viking_v4_v1_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        self.assertEqual(a.name, "VIKING_V4_V1")

    def test_viking_v4_v1_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        self.assertEqual(len(a), 12)

    def test_viking_v4_v1_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'V1_ED', 'V1_EPDIFF', 'V1_EPAR', 'V1_EC', 'V1_VFG', 'V1_ID',
                        'V1_IFILL', 'V1_USER_BIAS', 'V1_RELATIVE_TIME', 'V1_VGUARD',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }

        keys_set = set(a.keys())
        self.assertCountEqual(keys_set, expected_set)

    def test_viking_v4_v1_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4_V2"""

    def test_viking_v4_v2_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        self.assertEqual(a.name, "VIKING_V4_V2")

    def test_viking_v4_v2_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        self.assertEqual(len(a), 12)

    def test_viking_v4_v2_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'V2_THETA', 'V2_AMPLITUDE', 'V2_PHI', 'V2_PSI',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }
        keys_set = set(a.keys())
        self.assertSetEqual(keys_set, expected_set)

    def test_viking_v4_v2_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4H_SFA"""

    def test_viking_v4h_sfa_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        self.assertEqual(a.name, "VIKING_V4H_SFA")

    def test_viking_v4h_sfa_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        self.assertEqual(len(a), 12)

    def test_viking_v4h_sfa_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'DATETIME', 'MAGNETIC_SFA', 'ELECTRIC_SFA', 'FREQUENCY_SFA',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }

        keys_set = set(a.keys())
        self.assertCountEqual(keys_set, expected_set)

    def test_viking_v4h_sfa_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4H_FB"""

    def test_viking_v4h_fb_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        self.assertEqual(a.name, "VIKING_V4H_FB")

    def test_viking_v4h_fb_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        self.assertEqual(len(a), 12)

    def test_viking_v4h_fb_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'DATETIME', 'FREQUENCY_FB', 'ELECTRIC_FB', 'MAGNETIC_FB', 'T_Field',
                        'P_Field', 'UTC_T_Field', 'UTC_P_Field'}
        key_set = set(a.keys())
        self.assertSetEqual(key_set, expected_set)

    def test_viking_v4h_fba_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4L_FBL"""

    def test_viking_v4l_fbl_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        self.assertEqual(a.name, "VIKING_V4L_FBL")

    def test_viking_v4l_fbl_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_fbl_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'DATETIME', 'FREQUENCY_FBL', 'ELECTRIC_FBL',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }
        keys_set = set(a.keys())
        self.assertCountEqual(keys_set, expected_set)

    def test_viking_v4l_fbl_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4L_Ni"""

    def test_viking_v4l_ni_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        self.assertEqual(a.name, "VIKING_V4L_Ni")

    def test_viking_v4l_ni_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_ni_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'N1_PROBE', 'N2_PROBE',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }
        keys_set = set(a.keys())
        self.assertSetEqual(keys_set, expected_set)

    def test_viking_v4l_ni_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    def test_viking_v4l_ni_datetime_utc(self):
        print("### Testing VikingV4nData \"DATETIME_UTC\" key on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        dt = a["DATETIME_UTC"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 0, 393000))

    """VIKING_V4L_DFT"""

    def test_viking_v4l_dft_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        self.assertEqual(a.name, "VIKING_V4L_DFT")

    def test_viking_v4l_dft_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_dft_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                        'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                        'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                        'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                        'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                        "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                        "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                        "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                        'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                        'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                        'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                        'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                        'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                        'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                        'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                        'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                        'UTC_CALENDER_MONTH', 'DFT',
                        'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                        }
        keys_set = set(a.keys())
        self.assertSetEqual(keys_set, expected_set)

    def test_viking_v4l_dft_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    def test_viking_v4l_dft_datetime_utc(self):
        print("### Testing VikingV4nData \"DATETIME_UTC\" key on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        dt = a["DATETIME_UTC"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 0, 393000))

    """VIKING_V4L_WF"""

    def test_viking_v4l_wf_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        self.assertEqual(a.name, "VIKING_V4L_WF")

    def test_viking_v4l_wf_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_wf_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        expected_set = {'V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'RECORD_NUMBER',
                       'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                       'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'ABNORMAL_END_OF_SWEEP',
                       'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                       'BUFFER_NUMBER', 'SATELLITE_TIME_MSB', "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3",
                       "CCSDS_B4", "CCSDS_B5", "CCSDS_B6", "CCSDS_B7", "CCSDS_B8", "UTC_CCSDS_B0", "UTC_CCSDS_B1",
                       "UTC_CCSDS_B2", "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                       "UTC_CCSDS_B7", "UTC_CCSDS_B8",
                       'TM_LACK_AFTER_SWEEP', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                       'UTC_CALENDAR_DAY', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                       'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                       'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                       'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                       'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP',
                       'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CALENDAR_YEAR',
                       'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND',
                       'UTC_CALENDER_MONTH', 'WF1', 'WF2',
                       'UTC_P_Field', 'UTC_T_Field', 'P_Field', 'T_Field', 'DATETIME',
                       }
        keys_set = set(a.keys())
        self.assertSetEqual(keys_set, expected_set)

    def test_viking_v4l_wf_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    def test_viking_v4l_wf_datetime_utc(self):
        print("### Testing VikingV4nData \"DATETIME_UTC\" key on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        dt = a["DATETIME_UTC"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 0, 393000))
