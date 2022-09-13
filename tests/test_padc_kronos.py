# -*- coding: utf-8 -*-
import datetime

import pytest
from maser.data.padc.cassini.kronos import (
    freq_abc,
    fi_freq,
    ti_datetime,
    t97_datetime,
    ydh_datetime,
)

f_abc = {
    8: [
        3.9548,
        4.7729,
        5.7601,
        6.9516,
        8.3895,
        10.1248,
        12.2191,
        14.7465,
        17.7968,
        21.4779,
        25.9205,
        31.2821,
        37.7526,
        45.5616,
        54.9858,
        66.3593,
        80.0854,
        96.6507,
        116.6424,
        140.7693,
        169.8868,
        205.0270,
        247.4359,
        298.6168,
    ],
    16: [
        3.7732,
        4.1452,
        4.5537,
        5.0026,
        5.4956,
        6.0373,
        6.6324,
        7.2861,
        8.0043,
        8.7932,
        9.6599,
        10.6120,
        11.6580,
        12.8071,
        14.0694,
        15.4562,
        16.9796,
        18.6532,
        20.4918,
        22.5115,
        24.7304,
        27.1679,
        29.8458,
        32.7875,
        36.0192,
        39.5694,
        43.4696,
        47.7542,
        52.4611,
        57.6319,
        63.3124,
        69.5528,
        76.4083,
        83.9395,
        92.2130,
        101.3019,
        111.2868,
        122.2558,
        134.3059,
        147.5438,
        162.0864,
        178.0625,
        195.6132,
        214.8939,
        236.0749,
        259.3436,
        284.9058,
        312.9876,
    ],
    32: [
        3.6856,
        3.8630,
        4.0489,
        4.2437,
        4.4480,
        4.6620,
        4.8864,
        5.1215,
        5.3680,
        5.6263,
        5.8971,
        6.1809,
        6.4783,
        6.7901,
        7.1169,
        7.4594,
        7.8184,
        8.1946,
        8.5890,
        9.0023,
        9.4355,
        9.8896,
        10.3656,
        10.8644,
        11.3872,
        11.9352,
        12.5096,
        13.1116,
        13.7426,
        14.4040,
        15.0972,
        15.8237,
        16.5852,
        17.3834,
        18.2200,
        19.0968,
        20.0158,
        20.9791,
        21.9887,
        23.0469,
        24.1560,
        25.3185,
        26.5369,
        27.8140,
        29.1525,
        30.5555,
        32.0259,
        33.5672,
        35.1826,
        36.8757,
        38.6504,
        40.5104,
        42.4599,
        44.5033,
        46.6450,
        48.8898,
        51.2426,
        53.7086,
        56.2933,
        59.0024,
        61.8418,
        64.8179,
        67.9373,
        71.2067,
        74.6335,
        78.2252,
        81.9898,
        85.9355,
        90.0711,
        94.4057,
        98.9490,
        103.7109,
        108.7019,
        113.9331,
        119.4161,
        125.1629,
        131.1864,
        137.4996,
        144.1167,
        151.0523,
        158.3216,
        165.9408,
        173.9266,
        182.2967,
        191.0697,
        200.2648,
        209.9025,
        220.0039,
        230.5915,
        241.6886,
        253.3198,
        265.5107,
        278.2883,
        291.6808,
        305.7178,
        320.4303,
    ],
}


# Cassini/RPWS/HFR Kronos TESTS
def test_co_rpws_hfr_kronos__freq_abc__8():
    assert len(freq_abc(8)) == 8 * 3
    assert freq_abc(8) == f_abc[8]


def test_co_rpws_hfr_kronos__freq_abc__16():
    assert len(freq_abc(16)) == 16 * 3
    assert freq_abc(16) == f_abc[16]


def test_co_rpws_hfr_kronos__freq_abc__32():
    assert len(freq_abc(32)) == 32 * 3
    assert freq_abc(32) == f_abc[32]


def test_co_rpws_hfr_kronos__freq_abc__error():
    with pytest.raises(ValueError):
        freq_abc(0)


def test_co_rpws_hfr_kronos__fi_freq__abc():
    assert fi_freq(3200) == 3.6856
    assert fi_freq(10000800) == 17.7968
    assert fi_freq(20001615) == 312.9876


def test_co_rpws_hfr_kronos__fi_freq__hf():
    assert fi_freq(31000201) == 2506.25
    assert fi_freq(43000800) == 7489.0625


def test_co_rpws_hfr_kronos__ti_datetime():
    dt = ti_datetime(100000, 0)
    assert dt == datetime.datetime(1996, 1, 1)
    dt = ti_datetime(100100000, 0)
    assert dt == datetime.datetime(1997, 1, 1)
    dt = ti_datetime(186400, 0)
    assert dt == datetime.datetime(1996, 1, 2)
    dt = ti_datetime(200000, 1)
    assert dt == datetime.datetime(1996, 1, 2, 0, 0, 0, 10000)


def test_co_rpws_hfr_kronos__t97_datetime():
    assert t97_datetime(1) == datetime.datetime(1997, 1, 1)
    assert t97_datetime(365.5) == datetime.datetime(1997, 12, 31, 12, 0)
    assert t97_datetime(366) == datetime.datetime(1998, 1, 1)
    assert t97_datetime(4017) == datetime.datetime(2007, 12, 31)


def test_co_rpws_hfr_kronos__ydh_datetime__int():
    assert ydh_datetime(201218022) == datetime.datetime(2012, 6, 28, 22, 0)


def test_co_rpws_hfr_kronos__ydh_datetime__str():
    assert ydh_datetime("2012180.22") == datetime.datetime(2012, 6, 28, 22, 0)
