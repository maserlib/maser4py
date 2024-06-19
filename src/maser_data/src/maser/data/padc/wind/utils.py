# -*- coding: utf-8 -*-


def get_indices(isweep):
    """Get the list of data indices in raw data for a given sweep.

    Internal data format is a 1D data vector: a series of 64-steps raw sweeps, with repeating some frequencies.
    - 16 frequency steps repeated once (band-a)
        f(kHz) | 20, 24, 28, 32, 36, 40, 44, 48, 52, 60, 72, 80, 92, 104, 116, 136
        -------+--------------------------------------------------------------------
        index  | 63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54,  22,  38,   6

    - 8 frequency steps repeated twice (band-b)
        f(kHz) | 152, 176, 196, 224, 256, 292, 332, 376
        -------+-----------------------------------------
        index  |  29,  13,  21,   5,  28,  12,  20,   4
        index  |  61,  45,  53,  37,  60,  44,  52,  36

    - 8 frequency steps repeated four times (band-c)
        f(kHz) | 428, 484, 548, 624, 708, 804, 916, 1040
        -------+------------------------------------------
        index  |  11,   3,  10,   2,   9,   1,   8,   0
        index  |  27,  19,  26,  18,  25,  17,  24,  16
        index  |  43,  35,  42,  34,  41,  33,  40,  32
        index  |  59,  51,  58,  50,  57,  49,  56,  48

    Public data format is composed of 32-steps sweeps, with distinct frequencies.
    - band-a is repeated in each consecutive 4 sweeps
        [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
        [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
        [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
        [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
    - band-b is repeated in each consecutive 2 sweeps
        [29, 13, 21,  5, 28, 12, 20,  4]
        [29, 13, 21,  5, 28, 12, 20,  4]
        [61, 45, 53, 37, 60, 44, 52, 36]
        [61, 45, 53, 37, 60, 44, 52, 36]
    - band-c is not repeated
        [11,  3, 10,  2,  9,  1,  8,  0]
        [27, 19, 26, 18, 25, 17, 24, 16]
        [43, 35, 42, 34, 41, 33, 40, 32]
        [59, 51, 58, 50, 57, 49, 56, 48]

    :param isweep: sweep id in output data format
    :return: raw sweep id and list of indices within raw data sweep
    """
    isweep_raw = isweep // 4

    # band-a
    steps_band_a = [63, 31, 47, 15, 55, 23, 39, 7, 62, 30, 46, 14, 54, 22, 38, 6]

    # band-b (second set is +32 for each value)
    steps_band_b = [
        k + 32 * ((isweep // 2) % 2) for k in [29, 13, 21, 5, 28, 12, 20, 4]
    ]

    # band-c (other sets are +16,+32,+48 for each value)
    steps_band_c = [k + 16 * (isweep % 4) for k in [11, 3, 10, 2, 9, 1, 8, 0]]

    return isweep_raw, steps_band_a + steps_band_b + steps_band_c
