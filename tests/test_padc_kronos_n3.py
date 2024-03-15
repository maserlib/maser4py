# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import BinData
from maser.data.padc.cassini.data import (
    CoRpwsHfrKronosN3eData,
    CoRpwsHfrKronosN3dData,
    CoRpwsHfrKronosN2Data,
    CoRpwsHfrKronosN1Data,
)

from astropy.time import Time
from astropy.units import Quantity
from pathlib import Path
import xarray
from xarray.core.dataarray import DataArray

# import xarray

TEST_FILES = {
    "co_rpws_hfr_kronos_n3e": [
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.00",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.01",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.02",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.03",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.04",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.05",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.06",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.07",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.08",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.09",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.10",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.11",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.12",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.13",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.14",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.15",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.16",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.17",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.18",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.19",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.20",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.21",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.22",
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.23",
    ],
    "co_rpws_hfr_kronos_n3d": [
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.00",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.01",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.02",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.03",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.04",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.05",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.06",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.07",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.08",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.09",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.10",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.11",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.12",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.13",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.14",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.15",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.16",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.17",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.18",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.19",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.20",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.21",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.22",
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.23",
    ],
}

# Cassini/RPWS/HFR Kronos N3d TESTS ==== co_rpws_hfr_kronos_n3d


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3d_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3d"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosN3dData)
        assert data.level == "n3d"


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3_error_levels():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3d"]:
        data = Data(filepath=filepath)
        with pytest.raises(ValueError):
            data.levels("error")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3_levels():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3d"]:
        data = Data(filepath=filepath)
        n2 = data.levels("n2")
        n1 = data.levels("n1")
        assert isinstance(data._levels, dict)
        assert isinstance(n1, CoRpwsHfrKronosN1Data)
        assert isinstance(n2, CoRpwsHfrKronosN2Data)


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3_times():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3d"]:
        data = Data(filepath=filepath)
        times = data.times
        assert isinstance(times, Time)


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3_frequencies():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3d"]:
        data = Data(filepath=filepath)
        freqs = data.frequencies
        assert isinstance(freqs, list)
        assert isinstance(freqs[0], Quantity)
        assert freqs[0].unit == "kHz"


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3d_bin_dataset__as_xarray():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n3d"][0]
    data = Data(filepath=filepath)
    xarr = data.as_xarray()
    assert isinstance(xarr, xarray.Dataset)
    xarr_keys = xarr.keys()
    assert set(xarr_keys) == set(data._format["vars"].keys())
    for k in xarr_keys:
        assert isinstance(xarr[k], DataArray)
    assert set(data.dataset_keys) == set(list(xarr.keys()))


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3d_quicklook():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3d"]:
        # ql_path = BASEDIR.parent / "quicklook" / "kronos" / f"{filepath.name}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        # data.quicklook(ql_path)

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# Cassini/RPWS/HFR Kronos N3e TESTS ==== co_rpws_hfr_kronos_n3e


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3e_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3e"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosN3eData)
        assert data.level == "n3e"


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3e_bin_dataset__as_xarray():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n3e"][0]
    data = Data(filepath=filepath)
    xarr = data.as_xarray()
    assert isinstance(xarr, xarray.Dataset)
    xarr_keys = xarr.keys()
    assert set(xarr_keys) == set(data._format["vars"].keys())
    for k in xarr_keys:
        assert isinstance(xarr[k], DataArray)
    assert set(data.dataset_keys) == set(list(xarr.keys()))


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3e_quicklook():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3e"]:
        # ql_path = BASEDIR.parent / "quicklook" / "kronos" / f"{filepath.name}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        # data.quicklook(ql_path)

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
