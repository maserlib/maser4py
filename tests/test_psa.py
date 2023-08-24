# -*- coding: utf-8 -*-
from .constants import BASEDIR
from maser.data import Data
from maser.data.psa import (
    MexMMarsis3RdrAisV1Data,
    MexMMarsis3RdrAisExt4V1Data,
    MexMMarsis3RdrAisV1Sweep,
)
from maser.data.pds import Pds3Data
import pytest
from pathlib import Path
from astropy.units import Quantity
import xarray


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
    assert isinstance(data, MexMMarsis3RdrAisV1Data)
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
    assert freqs[0].value == 109377.0
    assert freqs.unit.name == "Hz"


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0__iter_method__sweeps(mex_data):
    data = mex_data
    sweep = next(data.sweeps)
    assert isinstance(sweep, MexMMarsis3RdrAisV1Sweep)
    assert sweep.time == data.times[0]
    assert len(sweep.frequencies) == len(data.frequencies)
    assert sweep.frequencies[0].value == 109377.0
    assert sweep.data.shape == (160, 80)
    assert set(sweep.header.keys()) == {
        "process_id",
        "attenuation",
        "band_number",
        "transmit_power",
        "data_type",
        "mode_selection",
    }


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0__as_xarray(mex_data):
    data = mex_data
    xr = data.as_xarray()
    assert isinstance(xr, xarray.Dataset)
    assert set(xr.keys()) == {"DEFAULT", "DEFAULT"}
    assert xr.coords.dims == {"time": 1057, "frequency": 160}
    assert xr["DEFAULT"].dims == ("frequency", "time")
    assert xr["DEFAULT"].shape == (160, 1057)
    assert xr["DEFAULT"].units == "W m^-2 Hz^-1"


@pytest.mark.test_data_required
def test_mex_m_marsis_3_rdr_ais_ext4_v1_0_quicklook():
    for dataset in TEST_FILES.keys():
        for filepath in TEST_FILES[dataset]:
            #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
            ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
            data = Data(filepath=filepath)
            data.quicklook(ql_path_tmp)
            #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
            assert ql_path_tmp.is_file()
            ql_path_tmp.unlink()
