# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import CdfData
from maser.data.padc.wind.data import (
    WindWavesRad1L3AkrData,
    WindWavesRad1L3DfV01Data,
    WindWavesRad1L3DfV02Data,
)
from astropy.units import Quantity
from astropy.time import Time
import xarray
from pathlib import Path


from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "wi_wa_rad1_l3-akr": [
        BASEDIR / "maser" / "wind" / "wi_wa_rad1_l3-akr_19990101_v01.cdf",
    ],
    "wi_wav_rad1_l3_df_v01": [
        BASEDIR / "maser" / "wind" / "wi_wa_rad1_l3_df_19950119_v01.cdf",
    ],
    "wi_wav_rad1_l3_df_v02": [
        BASEDIR / "maser" / "wind" / "wi_wa_rad1_l3_df_20230523_v02.cdf",
    ],
}


@pytest.fixture
def wind_waves_l3_akr_files():
    return TEST_FILES["wi_wa_rad1_l3-akr"]


@pytest.fixture
def wind_waves_l3_df_files():
    return TEST_FILES["wi_wav_rad1_l3_df_v01"] + TEST_FILES["wi_wav_rad1_l3_df_v02"]


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset(wind_waves_l3_akr_files):
    for data_file in wind_waves_l3_akr_files:
        data = Data(filepath=data_file)
        assert isinstance(data, CdfData)
        assert isinstance(data, WindWavesRad1L3AkrData)


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset__frequencies(wind_waves_l3_akr_files):
    for data_file in wind_waves_l3_akr_files:
        data = Data(filepath=data_file)
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 32
        assert data.frequencies.unit == "kHz"
        assert data.frequencies.value[0] == 20
        assert data.frequencies.value[-1] == 1040


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset__times(wind_waves_l3_akr_files):
    for data_file in wind_waves_l3_akr_files:
        data = Data(filepath=data_file)
        assert isinstance(data.times, Time)
        assert len(data.times) == 471
        assert data.times[0].iso == "1999-01-01 00:00:52.605"
        assert data.times[1].iso == "1999-01-01 00:03:55.867"


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset__as_xarray(wind_waves_l3_akr_files):
    for data_file in wind_waves_l3_akr_files:
        data = Data(filepath=data_file)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"FLUX_DENSITY", "SNR"}
        assert xr.coords.dims == {"time": 471, "frequency": 32}
        assert xr["SNR"].dims == ("frequency", "time")
        assert xr["SNR"].shape == (32, 471)
        assert xr["FLUX_DENSITY"].units == "Wm2Hz-1"


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_df_dataset(wind_waves_l3_df_files):
    for data_file in wind_waves_l3_df_files:
        data = Data(filepath=data_file)
        assert isinstance(data, CdfData)
        if data.dataset.endswith("v01"):
            assert isinstance(data, WindWavesRad1L3DfV01Data)
        elif data.dataset.endswith("v02"):
            assert isinstance(data, WindWavesRad1L3DfV02Data)
        else:
            assert False


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_df_dataset__frequencies(wind_waves_l3_df_files):
    for data_file in wind_waves_l3_df_files:
        data = Data(filepath=data_file)
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 32
        assert data.frequencies.unit == "kHz"


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_df_dataset__times(wind_waves_l3_df_files):
    for data_file in wind_waves_l3_df_files:
        data = Data(filepath=data_file)
        assert isinstance(data.times, Time)
        assert len(data.times) == int(len(data.file["Epoch"][...]) / 16)


@pytest.mark.test_data_required
def test_wind_waves_l3_df_dataset_quicklook(wind_waves_l3_df_files):
    for filepath in wind_waves_l3_df_files:
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
