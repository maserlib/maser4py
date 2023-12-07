# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data import (
    SorbetCdfData,
)
import pytest
from .fixtures import skip_if_spacepy_not_available
import xarray
from pathlib import Path

TEST_FILES = {
    "padc_bepi_sorbet": [
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_20211001_v00.cdf",
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_20211002_v00.cdf",
    ],
}


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_dataset():
    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SorbetCdfData)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet__times():
    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            if "20211001" in Data.dataset:
                assert len(data.times) == 16545
                assert data.times[0] == Time("2021-10-01 02:31:16.118866")
                assert data.times[-1] == Time("2021-10-02 00:04:35.337677")
            elif "20211002" in Data.dataset:
                assert len(data.times) == 18355
                assert data.times[0] == Time("2021-10-01 23:59:41.526116")
                assert data.times[-1] == Time("2021-10-02 23:22:48.744561")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet__frequencies():
    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 128
            assert data.frequencies[0].to(Unit("MHz")).value == pytest.approx(
                0.002554743
            )
            assert data.frequencies[-1].to(Unit("MHz")).value == pytest.approx(
                0.626286125
            )


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet__access_mode_file():
    from spacepy import pycdf

    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet__iter_method__mode_file():
    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        data = Data(filepath=filepath, access_mode="file")
        var_labels = [item for item in data]
        assert list(data.file) == var_labels
        print(var_labels)
        assert var_labels == [
            "Epoch",
            "delta_start_scan",
            "delta_end_scan",
            "MDP_TI",
            "sorbet_WPT_spectra",
            "Frequency",
        ]


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["padc_bepi_sorbet"][0],
            access_mode="toto",
        )


@pytest.mark.test_data_required
def test_padc_bepi_sorbet_dataset_as_xarray():
    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"sorbet_WPT_spectra", "sorbet_WPT_spectra"}
        if "20211001" in Data.dataset:
            assert xr["sorbet_WPT_spectra"].shape == (128, 16545)
        elif "20211002" in Data.dataset:
            assert xr["sorbet_WPT_spectra"].shape == (128, 18355)
        assert xr["sorbet_WPT_spectra"].attrs["units"] == "dB_ref_V^{2}/Hz"
        assert (
            xr["sorbet_WPT_spectra"].attrs["title"] == "SORBET Power Spectral Density"
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_padc_bepi_sorbet_dataset_quicklook():
    for filepath in TEST_FILES["padc_bepi_sorbet"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        data.quicklook(ql_path_tmp)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
