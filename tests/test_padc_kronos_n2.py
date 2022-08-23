# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import BinData
from maser.data.padc.cassini.data import CoRpwsHfrKronosN2Data

from astropy.time import Time
from astropy.units import Quantity

# import xarray

TEST_FILES = {
    "co_rpws_hfr_kronos_n2": [
        BASEDIR / "kronos" / "2012_091_180" / "n2" / "P2012180.20",
        BASEDIR / "kronos" / "2012_091_180" / "n2" / "P2012180.21",
        BASEDIR / "kronos" / "2012_091_180" / "n2" / "P2012180.22",
    ],
}


# Cassini/RPWS/HFR Kronos N2 TESTS ==== co_rpws_hfr_kronos_n2
@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n2"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosN2Data)
        assert data.level == "n2"


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__len():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n2"][0]
    data = Data(filepath=filepath)
    assert data._nsweep == 219
    assert data._nrecord == 78621
    assert data.file_size == 3537945


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__len_records():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n2"]:
        data = Data(filepath=filepath, access_mode="records")
        assert len(data) == data._nrecord


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__len_sweeps():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n2"]:
        data = Data(filepath=filepath, access_mode="sweeps")
        assert len(data) == data._nsweep


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__len_file():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n2"]:
        data = Data(filepath=filepath, access_mode="file")
        assert len(data) == data.file_size


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__times_sweeps():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n2"][0]
    data = Data(filepath=filepath)
    assert len(data.times) == data._nsweep
    assert isinstance(data.times, Time)
    assert data.times[0] == Time("2012-06-28T20:00:01.320")
    assert data.times[200] == Time("2012-06-28T20:54:57.300")
    assert data.times[-1] == Time("2012-06-28T20:59:45.300")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__times_records():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n2"][0]
    data = Data(filepath=filepath, access_mode="records")
    assert len(data.times) == data._nrecord
    assert isinstance(data.times, Time)
    assert data.times[0] == Time("2012-06-28T20:00:01.320")
    assert data.times[200] == Time("2012-06-28T20:00:01.320")
    assert data.times[2000] == Time("2012-06-28T20:01:37.320")
    assert data.times[-1] == Time("2012-06-28T20:59:45.300")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__frequencies_sweeps():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n2"][0]
    data = Data(filepath=filepath)
    assert len(data.times) == data._nsweep
    assert isinstance(data.frequencies, list)
    assert isinstance(data.frequencies[0], Quantity)
    assert data.frequencies[0][0].value == pytest.approx(3.6856)
    assert data.frequencies[-1][0].value == pytest.approx(3.6856)
    assert data.frequencies[-1][-1].value == pytest.approx(16025)
    assert data.frequencies[0].unit == "kHz"


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n2_bin_dataset__frequencies_records():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n2"][0]
    data = Data(filepath=filepath, access_mode="records")
    assert len(data.times) == data._nrecord
    assert isinstance(data.frequencies, Quantity)
    assert data.frequencies[0].value == pytest.approx(3.6856)
    assert data.frequencies[-1].value == pytest.approx(16025)
    assert data.frequencies.unit == "kHz"
