# -*- coding: utf-8 -*-

CCSDS_CDS_FIELDS = (
    [
        "CCSDS_PREAMBLE",
        "CCSDS_JULIAN_DAY_B1",
        "CCSDS_JULIAN_DAY_B2",
        "CCSDS_JULIAN_DAY_B3",
        "CCSDS_MILLISECONDS_OF_DAY_B0",
        "CCSDS_MILLISECONDS_OF_DAY_B1",
        "CCSDS_MILLISECONDS_OF_DAY_B2",
        "CCSDS_MILLISECONDS_OF_DAY_B3",
    ],
    # CCSDS_PREAMBLE [Int, 8 bits] = 76
    # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
    # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
    ">BBBBBBBB",
)

CCSDS_CCS_FIELDS = (
    [
        "CCSDS_PREAMBLE",
        "CCSDS_B0",  # year
        "CCSDS_B1",  # month
        "CCSDS_B2",  # day in month
        "CCSDS_B3",  # hour
        "CCSDS_B4",  # minute
        "CCSDS_B5",  # second
        "CCSDS_B6",  # 1e-2 sec
        "CCSDS_B7",  # 1e-4 sec
    ],
    # This dataset uses CCSDS-CCS Time Format.
    # year, month, day, hour, minute, second, CCSDS_B0*256 + CCSDS_B1
    ">BhBBBBBBB",
)

CALDATE_FIELDS = (
    [
        "CALEND_DATE_YEAR",
        "CALEND_DATE_MONTH",
        "CALEND_DATE_DAY",
        "CALEND_DATE_HOUR",
        "CALEND_DATE_MINUTE",
        "CALEND_DATE_SECOND",
    ],
    # CALEND_DATE fields YEAR, MONTH, DAY, HOUR, MINUTE, SECOND: all [Int, 16bits]
    ">hhhhhh",
)

ORBIT_FIELDS = (
    ["GSE_X", "GSE_Y", "GSE_Z"],
    # SPACECRAFT_COORDINATES fields GSE_X, GSE_Y, GSE_Z: all [Real, 32bits], in Earth Radii (GSE)
    ">fff",
)
