# -*- coding: utf-8 -*-
from .constants import BASEDIR
from maser.data import Data
from maser.data.psa import (
    MexMMarsis3RdrAisExt4V1Data,
)
from maser.data.pds import Pds3Data
import pytest
from astropy.units import Quantity


TEST_FILES = {
    "mex-m-marsis-3-rdr-ais-ext4-v1.0": [
        BASEDIR / "psa" / "mex" / "marsis" / "FRM_AIS_RDR_13714.LBL"
    ],
}


@pytest.fixture
def mex_data():
    return Data(filepath=TEST_FILES["mex-m-marsis-3-rdr-ais-ext4-v1.0"][0])


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0__dataset(mex_data):
    data = mex_data
    assert data.dataset == "MEX-M-MARSIS-3-RDR-AIS-EXT4-V1.0"
    assert isinstance(data, MexMMarsis3RdrAisExt4V1Data)
    assert isinstance(data, Pds3Data)


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0__times(mex_data):
    data = mex_data
    times = data.times
    assert len(times) == 1057
    assert times[0].isot == "2014-10-21T03:45:40.562"


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0__freqs(mex_data):
    data = mex_data
    freqs = data.frequencies
    assert len(freqs) == 160
    assert isinstance(freqs, Quantity)
    assert freqs[0].value == 109.4
    assert freqs.unit.name == "kHz"


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0__iter_method__sweeps(mex_data):
    data = mex_data
    time, freqs, signal = next(data.sweeps)
    assert time == data.times[0]
    assert len(freqs) == len(data.frequencies)
    assert freqs[0].value == 109.4
    assert signal.shape == (160, 80)
