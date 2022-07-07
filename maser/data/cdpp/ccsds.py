# -*- coding: utf-8 -*-

"""
Python module to define classes for CCSDS Date formats in use with CDPP deep archive data (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "14-NOV-2018"
__project__ = "MASER/CDPP"

__all__ = [
    "decode_ccsds_date",
    "CCSDSDate",
    "CCSDSDateCUC",
    "CCSDSDateCDS",
    "CCSDSDateCCS",
    "from_binary_coded_decimal",
    "to_binary_coded_decimal",
]

import datetime

# TODO: implement BCD for CCS (but ISEE3-SBH doesn't follow the CCS standard)
# TODO: fix MSB as described in the CCSDS standard - first bit read is least significant bit


def decode_ccsds_date(p_field, t_field, epoch=None) -> "CCSDSDate":
    """Decode a CCSDS time format into a CCSDSDate derived object.

    A CCSDS Date is composed of 2 fields: a time specification field (`t_field`) and a time code
    preamble field (`p_field`). The `p_field` uniquely identifies a specific time code format.

    The time code format recognized by this library are:
    - _CUC_: CCSDS unsegmented time code
    - _CDS_: CCSDS day segmented time code
    - _CCS_: CCSDS calendar segmented time code

    The return object is one of CCSDSDateCUC, CCSDSDateCDS or CCSDSDateCCS, depending on `p_field` content.

    The output  on the `p_field` input parameter
    :param p_field: (int)
    :param t_field: (bytearray)
    :param epoch: Time start epoch
    :return: CCSDSDate derived object
    """

    time_code_id = int((p_field & 14) // 2)
    if time_code_id == 1:
        return CCSDSDateCUC(p_field, t_field)  # This is CCSDS CUC level 1 format
    elif time_code_id == 2:
        raise NotImplementedError(
            "CCSDS CUC level 2"
        )  # This is CCSDS CUC level 2 format
    elif time_code_id == 4:
        return CCSDSDateCDS(
            p_field, t_field, epoch
        )  # This is CCSDS CDS format (could be level 1 or 2)
    elif time_code_id == 5:
        return CCSDSDateCCS(p_field, t_field)  # This is CCSDS CCS format
    elif time_code_id == 6:
        raise NotImplementedError(
            "CCSDS Agency Defined level 2"
        )  # This is CCSDS AgencyDefined format
    else:
        raise Exception("Illegal Time Code ID")  # This is for reserved and unknown


class CCSDSDate(object):
    """Base Class for CCSDS time format object.

    The CCSDSDate object is built out from 2 fields: `t_field` (time specification field) and `p_field` (time code
    preamble field). The `p_field` uniquely identifies a specific time code format.

    The time code format recognized by this library are:
    * _CUC_: CCSDS unsegmented time code
    * _CDS_: CCSDS day segmented time code
    * _CCS_: CCSDS calendar segmented time code

    Time code formats are also classified with a Level number:
    * _Level 1_: Complete Unambiguous Interpretation
    * _Level 2_: Partial Interpretation (Epoch must be provided externally)
    * _Level 3_: No Interpretation Except for Recognition of Increasing Time Value
    * _Level 4_: No Interpretation

    This module can currently decode CUC Level 1, CDS level 1 and 2, and CCS time code formats.

    This module doesn't deal with ASCII formatted time formats, in this case, use `datetime`, `dateutil`,
    or other equivalent modules.

    For more info on CCSDS time formats, refer to "TIME CODE FORMATS" CCSDS 301.0-B-3, Jan. 2002.
    The following points are particularly important in the decoding:
    * The `p_field` is encoded in _MSB (Most Significant Bit)_. This is interpreted as follows: when written as a string
    of `0` and `1`, the left-most bit is the least significant bit, labelled as `bit 0` (see page 9 of the "TIME CODE
    FORMATS" CCSDS document). The bits of the `p_field` byte should then be flipped before applying use standard
    bit-wise operations.
    * In CCS format, the values in the `t_field` are encoded in _Binary Coded Decimal (BCD)_. This means that the
    hexadecimal dump values shows the numbers to be read. For instance, the BCD value of `1980` is `6528` as its
    hexadecimal representation is `0x1980`. Note that some CDPP dataset, although using CCS time codes are not encoding
    the number with BCD.

    Args:
        p_field (int): time code preamble code.
        t_field (bytearray): time specification field (list of 8bit integers).

    Attributes:
        P_field (int): time code preamble code.
        T_field (list): time specification field (list of 8-bit integers).
        time_code_name (str): Time code name
        time_code_level (int): Time code level
        datetime (datetime.datetime): decoded datetime object
        time_scale (str): Time scale (UTC, TAI...)
        epoch_type (str): type of reference epoch (origin of time)
        time_epoch (datetime.datetime): Origin of time (CUC and CDS time formats only)
    """

    def __init__(self, p_field, t_field):
        self.P_field = p_field
        self.T_field = [b for b in t_field]

        # decoding P_FIELD
        self._extension_flag = (self.P_field & 1) == 1
        self._time_code_id = int((self.P_field & 14) / 2)

        # EXTENSION_FLAG = 0: 1 byte P_field
        # EXTENSION_FLAG = 1: 2 bytes P_field [NB: not sure it is used yet...]
        self._P_field_size = self._extension_flag + 1

        # names of TIME_CODE_ID
        time_code_level_values = [
            "_UNK_",
            "CUC",
            "CUC",
            "_UNK_",
            "CDS",
            "CCS",
            "AGENCY_DEFINED",
            "_UNK_",
        ]
        self.time_code_name = time_code_level_values[self._time_code_id]

        # levels of TIME_CODE_ID
        time_code_level_values = [0, 1, 2, 0, 0, 1, 2, 0]
        self.time_code_level = time_code_level_values[self._time_code_id]

        # preparing extra attributes used by derived classes
        self.datetime = datetime.datetime
        self.time_scale = ""
        self.time_epoch = datetime.datetime
        self.epoch_type = ""
        self._n_bytes_t_field = len(
            self.T_field
        )  # this value will be check by derived classes

    def _decode_t_field(self) -> datetime.datetime:
        return NotImplemented


class CCSDSDateCUC(CCSDSDate):
    """Class for CCSDS CUC (Level 1) time format object."""

    def __init__(self, p_field, t_field):
        CCSDSDate.__init__(self, p_field, t_field)

        self._n_bytes_coarse_time = int(((self.P_field & 48) / 16) + 1)
        self._n_bytes_fine_time = int((self.P_field & 192) / 64)
        if self._n_bytes_t_field != self._n_bytes_coarse_time + self._n_bytes_fine_time:
            raise Exception(
                "T_field length does match P_field time format specification"
            )
        self.time_scale = "TAI"

        self.epoch_type = "CCSDS"
        self.time_epoch = datetime.datetime(1958, 1, 1)
        self.datetime = self._decode_t_field()

    def _decode_t_field(self) -> datetime.datetime:
        """Return a datetime object out of a CUC T_field"""
        seconds = 0
        for item in self.T_field[0 : self._n_bytes_coarse_time]:
            seconds = seconds * 256 + item

        sub_seconds_fraction_counter = 0
        sub_seconds_fraction_total = 2 ** (8 * self._n_bytes_fine_time)
        for item in self.T_field[self._n_bytes_coarse_time :]:
            sub_seconds_fraction_counter = sub_seconds_fraction_counter * 256 + item

        microseconds = int(
            (sub_seconds_fraction_counter * 1e6) / sub_seconds_fraction_total
        )

        if self._n_bytes_fine_time == 3:
            print(
                "{}: {}".format(
                    "Warning",
                    "Python datetime module doesn't handle sub-microsecond accuracy.",
                )
            )

        return (
            self.time_epoch
            + datetime.timedelta(seconds=seconds)
            + datetime.timedelta(microseconds=microseconds)
        )


class CCSDSDateCDS(CCSDSDate):
    """Class for CCSDS CDS (Level 1) time format object."""

    def __init__(self, p_field, t_field, epoch=None):
        CCSDSDate.__init__(self, p_field, t_field)

        if self.P_field & 16 == 0:
            self.epoch_type = "CCSDS"
            self.time_epoch = datetime.datetime(1958, 1, 1)
            self.time_code_level = 1
        else:
            self.epoch_type = "AGENCY_DEFINED"
            self.time_code_level = 2
            self.time_epoch = epoch

        self._n_bytes_day = int(((self.P_field & 32) / 32) + 2)
        self._n_bytes_millisecond = 4
        self._n_bytes_sub_millisecond = int((self.P_field & 192) / 32)
        if (
            self._n_bytes_t_field
            != self._n_bytes_day
            + self._n_bytes_millisecond
            + self._n_bytes_sub_millisecond
        ):
            raise Exception(
                "T_field length does match P_field time format specification"
            )
        self.time_scale = "UTC"

        self.datetime = self._decode_t_field()

    def _decode_t_field(self) -> datetime.datetime:
        """Return a datetime object out of a CDS T_field"""
        days = 0
        for item in self.T_field[0 : self._n_bytes_day]:
            days = days * 256 + item

        millisec = 0
        for item in self.T_field[self._n_bytes_day : self._n_bytes_day + 4]:
            millisec = millisec * 256 + item

        sub_milli = 0
        for item in self.T_field[self._n_bytes_day + 4 :]:
            sub_milli = sub_milli * 256 + item

        seconds = millisec // 1000
        microsec = (millisec % 1000) * 1000 + sub_milli

        return (
            self.time_epoch
            + datetime.timedelta(days=days)
            + datetime.timedelta(seconds=seconds)
            + datetime.timedelta(microseconds=microsec)
        )


class CCSDSDateCCS(CCSDSDate):
    """Class for CCSDS CCS (Level 1) time format object."""

    def __init__(self, p_field, t_field):
        CCSDSDate.__init__(self, p_field, t_field)

        self.epoch_type = "N/A"
        self._calendar_variation_flag = self.P_field & 16 == 16
        self._resolution = int((self.P_field & 224) / 32)
        if self._n_bytes_t_field != 7 + self._resolution:
            raise Exception(
                "T_field length does match P_field time format specification"
            )
        self.time_scale = "UTC"

        self.datetime = self._decode_t_field()

    def _decode_t_field(self):
        """Return a datetime object out of a CCS T_field"""
        year = self.T_field[0] * 256 + self.T_field[1]
        hour = self.T_field[4]
        minute = self.T_field[5]
        second = self.T_field[6]
        if self._calendar_variation_flag:
            day = self.T_field[2] * 256 + self.T_field[3] - 1
            dt = datetime.datetime(
                year, 1, 1, hour, minute, second
            ) + datetime.timedelta(days=day)
        else:
            month = self.T_field[2]
            day = self.T_field[3]
            dt = datetime.datetime(year, month, day, hour, minute, second)

        sub_second = 0
        for item in self.T_field[7:]:
            sub_second = sub_second * 100 + int(item)
        sub_second = sub_second / (100**self._resolution)

        micro = int(sub_second * 1e6)
        if self._resolution > 4:
            print(
                "{}: {}".format(
                    "Warning",
                    "Python datetime module doesn't handle sub-microsecond accuracy.",
                )
            )

        return dt + datetime.timedelta(microseconds=micro)


def to_binary_coded_decimal(value=0) -> int:
    return int("0x{}".format(value), 16)


def from_binary_coded_decimal(value=0) -> int:
    return int(hex(value)[2:])
