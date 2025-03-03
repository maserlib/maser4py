# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data import (
    SorbetL1CdfTnr,
    SorbetL1CdfDbsc,
)
import pytest
from .fixtures import skip_if_spacepy_not_available
import xarray
from pathlib import Path

TEST_FILES = {
    "padc_bepi_sorbet_l1_tnr": [
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_20211001_v00.cdf",
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_20211002_v00.cdf",
    ],
    "padc_bepi_sorbet_l1_dbsc": [
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_bz-ex_complex-specdB-tnr_20220623_v00.cdf",
    ],
}


# Tests L1 TNR
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_tnr_dataset():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SorbetL1CdfTnr)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_tnr__times():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
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
def test_padc_bepi_sorbet_l1_tnr__frequencies():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
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
def test_padc_bepi_sorbet_l1_tnr__access_mode_file():
    from spacepy import pycdf

    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_tnr__iter_method__mode_file():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
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
def test_padc_bepi_sorbet_l1_tnr__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["padc_bepi_sorbet_l1_tnr"][0],
            access_mode="toto",
        )


@pytest.mark.test_data_required
def test_padc_bepi_sorbet_l1_tnr_dataset_as_xarray():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
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
def test_padc_bepi_sorbet_l1_tnr_dataset_quicklook():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_tnr"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# Tests L1 DBSC
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_dbsc_dataset():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SorbetL1CdfDbsc)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_dbsc__times():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 18875
            assert data.times[0] == Time("2022-06-22 23:59:43.025604")
            assert data.times[-1] == Time("2022-06-24 00:04:33.837921")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_dbsc__frequencies():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
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
def test_padc_bepi_sorbet_l1_dbsc__access_mode_file():
    from spacepy import pycdf

    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_dbsc__iter_method__mode_file():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
        data = Data(filepath=filepath, access_mode="file")
        var_labels = [item for item in data]
        assert list(data.file) == var_labels
        print(var_labels)
        assert var_labels == [
            "Epoch",
            "delta_start_scan",
            "delta_end_scan",
            "MDP_TI",
            "sorbet_dbsc_spectra",
            "Bz_Ex_cross_amplitude",
            "Bz_Ex_cross_phase",
            "Frequency",
        ]


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_padc_bepi_sorbet_l1_dbsc__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["padc_bepi_sorbet_l1_dbsc"][0],
            access_mode="toto",
        )


@pytest.mark.test_data_required
def test_padc_bepi_sorbet_l1_dbsc_dataset_as_xarray():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {
            "sorbet_dbsc_spectra",
            "Bz_Ex_cross_amplitude",
            "Bz_Ex_cross_phase",
        }
        assert xr["sorbet_dbsc_spectra"].shape == (128, 18875)
        assert xr["sorbet_dbsc_spectra"].attrs["units"] == "dB_ref_V^{2}/Hz"
        assert (
            xr["sorbet_dbsc_spectra"].attrs["title"] == "SORBET Power Spectral Density"
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_padc_bepi_sorbet_l1_dbsc_dataset_quicklook():
    for filepath in TEST_FILES["padc_bepi_sorbet_l1_dbsc"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
