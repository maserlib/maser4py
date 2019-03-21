import unittest
import datetime
import datetime

from maser.data.cdpp.ccsds import decode_ccsds_date, CCSDSDateCCS, CCSDSDateCDS, CCSDSDateCUC, \
    from_binary_coded_decimal, to_binary_coded_decimal


class CCSDSDateTest(unittest.TestCase):
    """Test case for CCSDSDate class"""

    def test_cdpp_ccsds_date_ccs_day_of_year_format(self):
        """Testing CCSDSDate CCS format class (Year-DoY option)"""
        p_field = 0b01111010
        t_field = bytearray.fromhex("07 e2 01 3d 10 3b 00 0b 16 21")  # [2018, 317, 16, 59, 00, 11, 22, 33]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCCS)
        self.assertEqual(c._extension_flag, False)
        self.assertEqual(c._time_code_id, 5)
        self.assertEqual(c.time_code_name, 'CCS')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'N/A')
        self.assertEqual(c._calendar_variation_flag, True)
        self.assertEqual(c._resolution, 3)
        self.assertEqual(c._n_bytes_t_field, len(t_field))
        self.assertEqual(c.time_scale, 'UTC')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 112233))

    def test_cdpp_ccsds_date_ccs_month_day_format(self):
        """Testing CCSDSDate CCS format class (Year-Month-Day option)"""
        p_field = 0b01101010
        t_field = bytearray.fromhex("07 e2 0b 0d 10 3b 00 0b 16 21")  # [2018, 11, 13, 16, 59, 00, 11, 22, 33]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCCS)
        self.assertEqual(c._extension_flag, False)
        self.assertEqual(c._time_code_id, 5)
        self.assertEqual(c.time_code_name, 'CCS')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'N/A')
        self.assertEqual(c._calendar_variation_flag, False)
        self.assertEqual(c._resolution, 3)
        self.assertEqual(c._n_bytes_t_field, len(t_field))
        self.assertEqual(c.time_scale, 'UTC')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 112233))

    def test_cdpp_ccsds_date_cds_short_day_segment_with_microsec_format(self):
        """Testing CCSDSDate CDS format class (short day segment and microsecond options)"""
        p_field = 0b01001000
        t_field = bytearray.fromhex("56 d7 03 A4 EC 90 00 e9")  # [2018, 11, 13, 16, 59, 00, 11, 22, 33]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCDS)
        self.assertEqual(c._extension_flag, False)
        self.assertEqual(c._time_code_id, 4)
        self.assertEqual(c.time_code_name, 'CDS')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_day, 2)
        self.assertEqual(c._n_bytes_millisecond, 4)
        self.assertEqual(c._n_bytes_sub_millisecond, 2)
        self.assertEqual(c._n_bytes_t_field, len(t_field))
        self.assertEqual(c.time_scale, 'UTC')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 112233))

    def test_cdpp_ccsds_date_cds_short_day_segment_format(self):
        """Testing CCSDSDate CDS format class (short day segment option)"""
        p_field = 0b00001000
        t_field = bytearray.fromhex("56 d7 03 A4 EC 90")  # [2018, 11, 13, 16, 59, 00, 11, 20, 00]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCDS)
        self.assertEqual(c._extension_flag, False)
        self.assertEqual(c._time_code_id, 4)
        self.assertEqual(c.time_code_name, 'CDS')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_day, 2)
        self.assertEqual(c._n_bytes_millisecond, 4)
        self.assertEqual(c._n_bytes_sub_millisecond, 0)
        self.assertEqual(c._n_bytes_t_field, len(t_field))
        self.assertEqual(c.time_scale, 'UTC')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 112000))

    def test_cdpp_ccsds_date_cds_long_day_segment_format(self):
        """Testing CCSDSDate CDS format class (long day segment option)"""
        p_field = 0b00101000
        t_field = bytearray.fromhex("01 02 0C 03 A4 EC 90")  # [2138, 11, 13, 16, 59, 00, 11, 20, 00]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCDS)
        self.assertEqual(c._extension_flag, False)
        self.assertEqual(c._time_code_id, 4)
        self.assertEqual(c.time_code_name, 'CDS')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_day, 3)
        self.assertEqual(c._n_bytes_millisecond, 4)
        self.assertEqual(c._n_bytes_sub_millisecond, 0)
        self.assertEqual(c._n_bytes_t_field, len(t_field))
        self.assertEqual(c.time_scale, 'UTC')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2138, 11, 13, 16, 59, 00, 112000))

    def test_cdpp_ccsds_date_cuc_subsec0(self):
        """Testing CCSDSDate CUC format (3 bytes sub-second segment) class"""
        p_field = 0b00110010
        t_field = bytearray.fromhex("72 7D 61 54")  # [2018, 11, 13, 16, 59, 00]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCUC)
        self.assertEqual(c._time_code_id, 1)
        self.assertEqual(c.time_code_name, 'CUC')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_coarse_time, 4)
        self.assertEqual(c._n_bytes_fine_time, 0)
        self.assertEqual(c.time_scale, 'TAI')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00))  # rounding issue

    def test_cdpp_ccsds_date_cuc_subsec1(self):
        """Testing CCSDSDate CUC format (3 bytes sub-second segment) class"""
        p_field = 0b01110010
        t_field = bytearray.fromhex("72 7D 61 54 1C")  # [2018, 11, 13, 16, 59, 00, 11, 22, 33]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCUC)
        self.assertEqual(c._time_code_id, 1)
        self.assertEqual(c.time_code_name, 'CUC')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_coarse_time, 4)
        self.assertEqual(c._n_bytes_fine_time, 1)
        self.assertEqual(c.time_scale, 'TAI')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 109375))  # precision too low for this test

    def test_cdpp_ccsds_date_cuc_subsec2(self):
        """Testing CCSDSDate CUC format (3 bytes sub-second segment) class"""
        p_field = 0b10110010
        t_field = bytearray.fromhex("72 7D 61 54 1C BB")  # [2018, 11, 13, 16, 59, 00, 11, 22, 33]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCUC)
        self.assertEqual(c._time_code_id, 1)
        self.assertEqual(c.time_code_name, 'CUC')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_coarse_time, 4)
        self.assertEqual(c._n_bytes_fine_time, 2)
        self.assertEqual(c.time_scale, 'TAI')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 112228))  # precision too low for this test

    def test_cdpp_ccsds_date_cuc_subsec3(self):
        """Testing CCSDSDate CUC format (3 bytes sub-second segment) class"""
        p_field = 0b11110010
        t_field = bytearray.fromhex("72 7D 61 54 1C BB 4D")  # [2018, 11, 13, 16, 59, 00, 11, 22, 33]
        c = decode_ccsds_date(p_field, t_field)
        self.assertIsInstance(c, CCSDSDateCUC)
        self.assertEqual(c._time_code_id, 1)
        self.assertEqual(c.time_code_name, 'CUC')
        self.assertEqual(c.time_code_level, 1)
        self.assertEqual(c.epoch_type, 'CCSDS')
        self.assertEqual(c._n_bytes_coarse_time, 4)
        self.assertEqual(c._n_bytes_fine_time, 3)
        self.assertEqual(c.time_scale, 'TAI')
        dt = c.datetime
        self.assertIsInstance(c.datetime, datetime.datetime)
        self.assertEqual(dt, datetime.datetime(2018, 11, 13, 16, 59, 00, 112232))  # rounding issue


class CCSDSConversionBCD(unittest.TestCase):
    """Class to test Binary Coded Decimal conversion
    """

    def test_from_bcd(self):
        self.assertEqual(1980, from_binary_coded_decimal(6528))

    def test_to_bcd(self):
        self.assertEqual(6528, to_binary_coded_decimal(1980))
