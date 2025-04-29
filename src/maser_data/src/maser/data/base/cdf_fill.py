#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module to fill CDF data with FILLVAL values as expected by ISTP standards.
"""

__all__ = ["CDFToFill", "fill_records", "fill_dict", "Singleton"]


class Singleton(type):
    """
    A metaclass to create singletons, i.e classes that can have at most only
    one instance created at a given time.
    """

    def __call__(cls, *args, **kwargs):
        """
        Check that an instance is already stored before creating a new one.
        """
        if hasattr(cls, "instance"):
            return cls.instance

        cls.instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.instance


def fill_records(records):
    _filler(records, records.dtype.names)


def fill_dict(records):
    _filler(records, records.keys())


def _filler(records, names):
    # the converter
    converter = CDFToFill()

    # loop over fields
    for name in names:
        # dtype of the record
        dtype = records[name].dtype.name

        # the to fill with
        value = converter(dtype)

        # fill with value
        records[name].fill(value)


class CDFToFill(object, metaclass=Singleton):
    """
    To create a mapping between the CDF units and their fill values.
    """

    def __init__(self):
        self.mapping = {
            "CDF_BYTE": -128,
            "CDF_INT1": -128,
            "int8": -128,
            "CDF_UINT1": 255,
            "uint8": 255,
            "CDF_INT2": -32768,
            "int16": -32768,
            "CDF_UINT2": 65535,
            "uint16": 65535,
            "CDF_INT4": -2147483648,
            "int32": -2147483648,
            "CDF_UINT4": 4294967295,
            "uint32": 4294967295,
            "CDF_INT8": -9223372036854775808,
            "int64": -9223372036854775808,
            "uint64": 18446744073709551615,
            "float": -1e31,
            "float16": -1e31,
            "CDF_REAL4": -1e31,
            "CDF_FLOAT": -1e31,
            "float32": -1e31,
            "CDF_REAL8": -1e31,
            "CDF_DOUBLE": -1e31,
            "float64": -1e31,
            "CDF_EPOCH": 0.0,
            "CDF_TIME_TT2000": -9223372036854775808,
            "CDF_CHAR": " ",
            "CDF_UCHAR": " ",
        }

        self.validmin_mapping = {
            "CDF_BYTE": -127,
            "CDF_INT1": -127,
            "CDF_UINT1": 0,
            "CDF_INT2": -32767,
            "CDF_UINT2": 0,
            "CDF_INT4": -2147483647,
            "CDF_UINT4": 0,
            "CDF_INT8": -9223372036854775807,
            "CDF_REAL4": -1e30,
            "CDF_FLOAT": -1e30,
            "CDF_REAL8": -1e30,
            "CDF_DOUBLE": -1e30,
            "CDF_TIME_TT2000": -9223372036854775807,
        }

        self.validmax_mapping = {
            "CDF_BYTE": 127,
            "CDF_INT1": 127,
            "CDF_UINT1": 254,
            "CDF_INT2": 32767,
            "CDF_UINT2": 65534,
            "CDF_INT4": 2147483647,
            "CDF_UINT4": 4294967294,
            "CDF_INT8": 9223372036854775807,
            "CDF_REAL4": 3.4028235e38,
            "CDF_FLOAT": 3.4028235e38,
            "CDF_REAL8": 1.7976931348623157e308,
            "CDF_DOUBLE": 1.7976931348623157e308,
            "CDF_TIME_TT2000": 9223372036854775807,
        }

    def __call__(self, value):
        if value not in self.mapping:
            # print('ERROR - {0} fill type not mapped'.format(value))
            return
        return self.mapping[value]

    def validmin(self, value):
        if value not in self.validmin_mapping:
            # print('ERROR - {0} validmin type not mapped'.format(value))
            return
        return self.validmin_mapping[value]

    def validmax(self, value):
        if value not in self.validmax_mapping:
            # print('ERROR - {0} validmax type not mapped'.format(value))
            return
        return self.validmax_mapping[value]
