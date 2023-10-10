# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.rpw import RpwLfrSurvBp1, RpwTnrSurv, RpwHfrSurv
from astropy.time import Time
from astropy.units import Quantity, Unit
from pathlib import Path
import xarray
from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "solo_L2_rpw-lfr-surv-bp1": [
        BASEDIR / "solo" / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf"
    ],
    "solo_L2_rpw-tnr-surv": [
        BASEDIR / "solo" / "rpw" / "solo_L2_rpw-tnr-surv_20220101_V02.cdf"
    ],
    "solo_L2_rpw-hfr-surv": [
        BASEDIR / "solo" / "rpw" / "solo_L2_rpw-hfr-surv_20220101_V01.cdf"
    ],
}

# TEST solo_L2_rpw-lfr-surv-bp1
# =============================

# create a decorator to test each file in the list
for_each_test_file = pytest.mark.parametrize(
    "filepath", TEST_FILES["solo_L2_rpw-lfr-surv-bp1"]
)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, RpwLfrSurvBp1)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert list(data.times.keys()) == ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]
        assert isinstance(data.times["B_F0"], Time)
        assert len(data.times["B_F0"]) == 86380
        assert data.times["B_F0"][0] == Time("2020-12-27 00:00:45.209203")
        assert data.times["B_F0"][-1] == Time("2020-12-28 00:00:44.618985")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert list(data.frequencies.keys()) == ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]
        assert isinstance(data.frequencies["B_F0"], Quantity)
        assert len(data.frequencies["B_F0"]) == 22
        assert data.frequencies["B_F0"][0].to(Unit("Hz")).value == pytest.approx(1776)
        assert data.frequencies["B_F0"][-1].to(Unit("Hz")).value == pytest.approx(9840)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert len(sweep) == 3
        assert isinstance(sweep[0], dict)
        assert isinstance(sweep[1], Time)
        assert isinstance(sweep[2], Quantity)
        assert list(sweep[0].keys()) == ["PB", "PE", "DOP", "ELLIP", "SX_REA"]
        assert len(sweep[2]) == 26


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        datasets = data.as_xarray()

        expected_keys = ["PB", "PE", "DOP", "ELLIP", "SX_REA"]
        expected_frequency_ranges = ["B_F1", "B_F0"]
        expected_full_keys = []
        for keys in expected_keys:
            for freq in expected_frequency_ranges:
                expected_full_keys.append(keys + "_" + freq)

        # check the sweep content
        assert len(datasets.keys()) == 5 * 2
        # assert sorted(list(datasets.keys())) == sorted(expected_keys)
        # assert list(datasets[expected_keys[0]].keys()) == expected_frequency_ranges
        assert sorted(list(datasets.keys())) == sorted(expected_full_keys)

        test_array = datasets[expected_keys[0] + "_" + expected_frequency_ranges[0]]
        assert isinstance(test_array, xarray.DataArray)
        assert test_array.coords["frequency"][0] == pytest.approx(120)
        assert test_array.attrs["units"] == "nT^2/Hz"
        assert test_array.dropna(dim="time", how="all").data[0][0] == pytest.approx(
            5.73584540e-08
        )


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_data_dataset_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data.quicklook(ql_path_tmp)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# TEST solo_L2_rpw-tnr-surv
# =============================

# create a decorator to test each file in the list
for_each_test_file = pytest.mark.parametrize(
    "filepath", TEST_FILES["solo_L2_rpw-tnr-surv"]
)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_tnr_surv_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, RpwTnrSurv)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_tnr_surv_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 172452
        assert data.times[0] == Time("2022-01-01 00:01:26.830833")
        assert data.times[-1] == Time("2022-01-01 00:01:26.324603")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_tnr_surv_dataset__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 128
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(3992)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(978572)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_tnr_surv_dataset__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert len(sweep) == 5
        assert isinstance(sweep[0], dict)
        assert isinstance(sweep[1], Time)
        assert isinstance(sweep[2], Quantity)
        assert list(sweep[0].keys()) == [
            "Epoch",
            "VOLTAGE_SPECTRAL_POWER1",
            "VOLTAGE_SPECTRAL_POWER2",
            "FLUX_DENSITY1",
            "FLUX_DENSITY2",
            "MAGNETIC_SPECTRAL_POWER1",
            "MAGNETIC_SPECTRAL_POWER2",
        ]
        assert len(sweep[2]) == 128


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_tnr_surv_data__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        datasets = data.as_xarray()

        expected_keys = ["VOLTAGE_SPECTRAL_POWER"]

        # check the sweep content
        assert len(datasets.keys()) == 1
        assert sorted(list(datasets.keys())) == sorted(expected_keys)

        test_array = datasets[expected_keys[0]][0]
        assert isinstance(test_array, xarray.DataArray)
        assert test_array.coords["frequency"][0][0] == pytest.approx(3991)
        assert test_array.attrs["units"] == "V^2/Hz"
        assert test_array.data[0][0] == pytest.approx(2.1229058431454354e-11)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_tnr_surv_data_dataset_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data.quicklook(ql_path_tmp)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# TEST solo_L2_rpw-hfr-surv
# =============================

# create a decorator to test each file in the list
for_each_test_file = pytest.mark.parametrize(
    "filepath", TEST_FILES["solo_L2_rpw-hfr-surv"]
)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_hfr_surv_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, RpwHfrSurv)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_hfr_surv_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 26871
        assert data.times[0] == Time("2021-12-31 23:56:21.686369")
        assert data.times[-1] == Time("2022-01-01 23:56:13.127199")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_hfr_surv_dataset__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 192
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(375000)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(16325000)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_hfr_surv_dataset__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert len(sweep) == 5
        assert isinstance(sweep[0], dict)
        assert isinstance(sweep[1], Time)
        assert isinstance(sweep[2], Quantity)
        assert list(sweep[0].keys()) == [
            "VOLTAGE_SPECTRAL_POWER1",
            "VOLTAGE_SPECTRAL_POWER2",
        ]
        assert len(sweep[2]) == 40
        assert list(sweep[3]) == ["V2-V3", "HF_V2-V3"]
        assert sweep[4] == "SURVEY_BURST"


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_hfr_surv_data__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        datasets = data.as_xarray()

        expected_keys = ["VOLTAGE_SPECTRAL_POWER"]

        # check the sweep content
        assert len(datasets.keys()) == 1
        assert sorted(list(datasets.keys())) == sorted(expected_keys)

        test_array = datasets[expected_keys[0]][0]
        assert isinstance(test_array, xarray.DataArray)
        assert test_array.coords["frequency"][0] == pytest.approx(6525)
        assert test_array.attrs["units"] == "V^2/Hz"
        assert test_array.data[110000] == pytest.approx(4.8739396889859025e-15)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_hfr_surv_data_dataset_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data.quicklook(ql_path_tmp)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
