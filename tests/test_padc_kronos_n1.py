# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import BinData
from maser.data.padc.cassini.data import CoRpwsHfrKronosN1Data, CoRpwsHfrKronosDataSweep

from astropy.time import Time
from astropy.units import Quantity, Unit

from xarray.core.dataarray import DataArray

TEST_FILES = {
    "co_rpws_hfr_kronos_n1": [
        BASEDIR / "kronos" / "2012_091_180" / "n1" / "R2012180.20",
        BASEDIR / "kronos" / "2012_091_180" / "n1" / "R2012180.21",
        BASEDIR / "kronos" / "2012_091_180" / "n1" / "R2012180.22",
        BASEDIR / "kronos" / "2012_181_270" / "n1" / "R2012181.22",
    ],
}


# Cassini/RPWS/HFR Kronos N1 TESTS ==== co_rpws_hfr_kronos_n1
@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosN1Data)
        assert data.level == "n1"
        assert data._ydh == filepath.name[-10:]


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath)
    assert data._nsweep == 219
    assert data._nrecord == 78621
    assert data.file_size == 2201388


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len_records():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n1"]:
        data = Data(filepath=filepath, access_mode="records")
        assert len(data) == data._nrecord


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len_sweeps():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n1"]:
        data = Data(filepath=filepath, access_mode="sweeps")
        assert len(data) == data._nsweep


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len_file():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n1"]:
        data = Data(filepath=filepath, access_mode="file")
        assert len(data) == data.file_size


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__times_sweeps():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath)
    assert len(data.times) == data._nsweep
    assert isinstance(data.times, Time)
    assert data._data["c"][0] == data.times[0].to_datetime().microsecond / 10000
    assert data._data["c"][-1] == data.times[-1].to_datetime().microsecond / 10000
    assert data.times[0] == Time("2012-06-28T20:00:01.320")
    assert data.times[200] == Time("2012-06-28T20:54:57.300")
    assert data.times[-1] == Time("2012-06-28T20:59:45.300")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__times_records():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath, access_mode="records")
    assert len(data.times) == data._nrecord
    assert isinstance(data.times, Time)
    assert data.times[0] == Time("2012-06-28T20:00:01.320")
    assert data.times[200] == Time("2012-06-28T20:00:01.320")
    assert data.times[2000] == Time("2012-06-28T20:01:37.320")
    assert data.times[-1] == Time("2012-06-28T20:59:45.300")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__frequencies_sweeps():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath)
    assert len(data.times) == data._nsweep
    assert isinstance(data.frequencies, list)
    assert isinstance(data.frequencies[0], Quantity)
    assert data.frequencies[0][0] == 3.6856 * Unit("kHz")
    assert data.frequencies[-1][0] == 3.6856 * Unit("kHz")
    assert data.frequencies[-1][-1] == 16025 * Unit("kHz")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__frequencies_records():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath, access_mode="records")
    assert len(data.times) == data._nrecord
    assert isinstance(data.frequencies, Quantity)
    assert data.frequencies[0] == 3.6856 * Unit("kHz")
    assert data.frequencies[-1] == 16025 * Unit("kHz")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__sweeps__header():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n1"]:
        data = Data(filepath=filepath)
        for i, s in enumerate(data.sweeps):
            assert isinstance(s, CoRpwsHfrKronosDataSweep)
            assert all(df == sf for df, sf in zip(data.frequencies[i], s.frequencies))
            assert data.times[i] == s.time


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__sweep_modes():
    sweep_mode_mask_lens = [1, 1, 1, 3]
    for sweep_mode_mask_len, filepath in zip(
        sweep_mode_mask_lens, TEST_FILES["co_rpws_hfr_kronos_n1"]
    ):
        data = Data(filepath=filepath)
        assert len(data.sweep_mode_masks) == sweep_mode_mask_len


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__as_xarray():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath)
    xarr = data.as_xarray()
    xarr_keys = xarr.keys()
    assert set(xarr_keys) == set(data._format["record_def"]["fields"])
    for k in xarr_keys:
        assert isinstance(xarr[k], DataArray)


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__records_data():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath)
    assert all(dd == rd for dd, rd in zip(data._data, data.records))
