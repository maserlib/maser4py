# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.rpw import RpwLfrSurvBp1, RpwTnrSurv, RpwHfrSurv
from astropy.time import Time, TimeDelta
from astropy.units import Quantity, Unit
from pathlib import Path
import xarray
from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "solo_L2_rpw-lfr-surv-bp1": [
        BASEDIR / "solo" / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf",
        BASEDIR / "solo" / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20220326_V02.cdf",
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
        assert isinstance(data.times, Time)
        if "20201227" in str(filepath):
            assert list(data.delta_times.keys()) == [
                "B_F0",
                "B_F1",
            ]  # ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]
            assert len(data.delta_times["B_F0"]) == 86380
            assert len(data.delta_times["B_F1"]) == 86380
            assert data.delta_times["B_F0"][0] + data.times[0] == Time(
                "2020-12-27 00:00:45.209203"
            )
            assert data.delta_times["B_F0"][-1] + data.times[-1] == Time(
                "2020-12-28 00:00:44.618985"
            )
            assert data.delta_times["B_F1"][0] + data.times[0] == Time(
                "2020-12-27 00:00:45.209371"
            )
            assert data.delta_times["B_F1"][-1] + data.times[-1] == Time(
                "2020-12-28 00:00:44.618985"
            )
            assert data.delta_times["B_F0"][1] + data.times[1] == Time(
                "2020-12-27 00:00:46.209144"
            )
            assert data.delta_times["B_F1"][1] + data.times[1] == Time(
                "2020-12-27 00:00:46.209311"
            )
        elif "20220326" in str(filepath):
            assert list(data.delta_times.keys()) == [
                "B_F0",
                "B_F1",
                "N_F0",
                "N_F1",
                "N_F2",
            ]
            assert len(data.delta_times["B_F0"]) == 24352
            assert len(data.delta_times["B_F1"]) == 24352
            assert data.delta_times["B_F0"][0] + data.times[0] == Time(
                "2022-03-26 00:01:47.986052"
            )
        assert isinstance(data.delta_times["B_F0"], TimeDelta)
        assert max(abs(data.delta_times["B_F1"])) < TimeDelta(0.0002 * Unit("s"))
        assert max(abs(data.delta_times["B_F0"])) < TimeDelta(0.0002 * Unit("s"))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert list(data.frequencies.keys()) == [
            "N_F0",
            "B_F0",
            "N_F1",
            "B_F1",
            "N_F2",
        ]  # ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]
        assert isinstance(data.frequencies["B_F0"], Quantity)
        if "20201227" in str(filepath):
            assert len(data.frequencies["B_F0"]) == 22
            assert len(data.frequencies["B_F1"]) == 26
            assert len(data.frequencies["N_F0"]) == 0
            assert len(data.frequencies["N_F1"]) == 0
            assert len(data.frequencies["N_F2"]) == 0
        elif "20220326" in str(filepath):
            assert len(data.frequencies["B_F0"]) == 22
            assert len(data.frequencies["B_F1"]) == 26
            assert len(data.frequencies["N_F0"]) == 11
            assert len(data.frequencies["N_F1"]) == 13
            assert len(data.frequencies["N_F2"]) == 12
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
        assert list(sweep[0].keys()) == ["PB", "PE", "DOP", "ELLIP", "SX_REA"]
        # assert isinstance(sweep[0]["PB"], Quantity)
        if "20201227" in str(filepath):
            assert len(sweep[0]["PB"]) == 22  # 26
        elif "20220326" in str(filepath):
            assert len(sweep[0]["PB"]) == 11  # 26
        assert isinstance(sweep[1], Time)
        if "20201227" in str(filepath):
            assert sweep[1] == Time(
                "2020-12-27 00:00:45.209203"
            )  # Time("2020-12-27 00:00:45.209371")
        elif "20220326" in str(filepath):
            assert sweep[1] == Time("2022-03-26 00:01:47.986052")
        assert isinstance(sweep[2], Quantity)
        if "20201227" in str(filepath):
            assert len(sweep[2]) == 22  # 26
            assert sweep[2][0].to(Unit("Hz")).value == pytest.approx(1776)  # 120
        elif "20220326" in str(filepath):
            assert len(sweep[2]) == 11  # 26
            assert sweep[2][0].to(Unit("Hz")).value == pytest.approx(1968)  # 120


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_rpw_lfr_surv_bp1_dataset__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        datasets = data.as_xarray()

        expected_keys = ["PB", "PE", "DOP", "ELLIP", "SX_REA", "DELTA_TIMES", "MODE_NB"]
        # if "20201227" in str(filepath):
        #     expected_frequency_ranges = ["B_F0", "B_F1"]
        # elif "20220326" in str(filepath):
        #     expected_frequency_ranges = ["N_F0", "B_F0", "N_F1", "B_F1", "N_F2"]
        # expected_full_keys = []
        # for keys in expected_keys:
        #     for freq in expected_frequency_ranges:
        #         expected_full_keys.append(keys + "_" + freq)

        # check the sweep content
        assert len(datasets.keys()) == 7  # 5
        # assert sorted(list(datasets.keys())) == sorted(expected_keys)
        # assert list(datasets[expected_keys[0]].keys()) == expected_frequency_ranges
        assert sorted(list(datasets.keys())) == sorted(expected_keys)

        test_array = datasets[expected_keys[0]]
        assert isinstance(test_array, xarray.DataArray)
        if "20201227" in str(filepath):
            assert test_array.coords["frequency"][0] == pytest.approx(120)
            # assert len(test_array.values) == 108175
            assert len(test_array.values) == 48  # 86380 now freq dim instead of time
        elif "20220326" in str(filepath):
            assert test_array.coords["frequency"][0] == pytest.approx(10.5)
            # assert len(test_array.values) == 108175
            assert len(test_array.values) == 84  # 24352 now freq dim instead of time
        assert test_array.attrs["units"] == "nT^2/Hz"
        # assert test_array.attrs == {"units" : "nT^2/Hz"}
        if "20201227" in str(filepath):
            assert test_array.dropna(dim="time", how="all").data[0][0] == pytest.approx(
                5.73584540e-08
            )
        elif "20220326" in str(filepath):
            assert test_array.dropna(dim="time", how="all").data[0][0] == pytest.approx(
                0.000860668411803
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
