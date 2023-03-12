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

# import xarray

TEST_FILES = {
    "co_rpws_hfr_kronos_n3e": [
        BASEDIR / "kronos" / "2012_181_270" / "n3e" / "N3e_dsq2012181.00",
    ],
    "co_rpws_hfr_kronos_n3d": [
        BASEDIR / "kronos" / "2012_181_270" / "n3d" / "N3d_dsq2012181.00",
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


# Cassini/RPWS/HFR Kronos N3e TESTS ==== co_rpws_hfr_kronos_n3e


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n3e_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n3e"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosN3eData)
        assert data.level == "n3e"
