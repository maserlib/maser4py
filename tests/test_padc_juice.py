# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import CdfData
from maser.data.padc.juice import JuiceRPWIhfL1aCdfSID2, JuiceRPWIhfL1aCdfSID3
from maser.data.padc.juice import JuiceRPWIhfL1aCdfSID4, JuiceRPWIhfL1aCdfSID20
from maser.data.padc.juice import JuiceRPWIhfL1aCdfSID5, JuiceRPWIhfL1aCdfSID21
from maser.data.padc.juice import JuiceRPWIhfL1aCdfSID6, JuiceRPWIhfL1aCdfSID22
from maser.data.padc.juice import JuiceRPWIhfL1aCdfSID7, JuiceRPWIhfL1aCdfSID23
from astropy.time import Time
from astropy.units import Quantity, Unit
from pathlib import Path
import xarray
from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "jui_rpwi_l1a_SID2": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID2_20000101T000154-20000101T000454_V01___SID02_20241021-1026.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID3": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID3_20000101T000046-20000101T000518_V01___SID03-3ch-comp3-20241015-2313.ccs.cdf",
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID3_20000101T000049-20000101T000231_V01___SID03-3ch-comp0-20231117-1424.ccs.cdf",
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID3_20000101T000055-20000101T000453_V01___SID03-3ch-comp2-20241014-1132.ccs.cdf",
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID3_20000101T000131-20000101T000529_V01___SID03-3ch-comp1-20241014-2138.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID4": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID4_20000101T000057-20000101T000119_V01___SID04-20-comp0-20231117-1529.ccs.cdf",
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID4_20000101T000100-20000101T000144_V01___SID04-20-comp1-20231117-1532.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID20": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID20_20000101T000046-20000101T000127_V01___SID04-20-comp0-20231117-1529.ccs.cdf",
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID20_20000101T000050-20000101T000147_V01___SID04-20-comp1-20231117-1532.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID5": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID5_20000101T000044-20000101T000144_V01___SID05-21_20231117-1611.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID21": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID21_20000101T000044-20000101T000144_V01___SID05-21_20231117-1611.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID6": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID6_20000101T002625-20000101T003025_V01___SID06-22_20231024-0049.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID22": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID22_20000101T002555-20000101T003025_V01___SID06-22_20231024-0049.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID7": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID7_20000101T000047-20000101T000047_V01___SID07-23_20231024-0024.ccs.cdf",
    ],
    "jui_rpwi_l1a_SID23": [
        BASEDIR
        / "maser"
        / "juice"
        / "l1a"
        / "JUICE_L1a_RPWI-HF-SID23_20000101T000047-20000101T000047_V01___SID07-23_20231024-0024.ccs.cdf",
    ],
    "jui_rpwi_l1b": [],
    "jui_rpwi_l2": [],
}

# create a decorator to test each file in the list
for_each_test_file_l1asid2 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID2"]
)
for_each_test_file_l1asid3 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID3"]
)
for_each_test_file_l1asid4 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID4"]
)
for_each_test_file_l1asid20 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID20"]
)
for_each_test_file_l1asid5 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID5"]
)
for_each_test_file_l1asid21 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID21"]
)
for_each_test_file_l1asid6 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID6"]
)
for_each_test_file_l1asid22 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID22"]
)
for_each_test_file_l1asid7 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID7"]
)
for_each_test_file_l1asid23 = pytest.mark.parametrize(
    "filepath", TEST_FILES["jui_rpwi_l1a_SID23"]
)
for_each_test_file_l1b = pytest.mark.parametrize("filepath", TEST_FILES["jui_rpwi_l1b"])
for_each_test_file_l2 = pytest.mark.parametrize("filepath", TEST_FILES["jui_rpwi_l2"])


# L1a
# SID2
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid2
def test_jui_rpwi_l1a_sid2_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID2)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid2
def test_jui_rpwi_l1a_sid2_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 7  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:01:54.268628"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:04:54.268628")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid2
def test_jui_rpwi_l1a_sid2__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 32767
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            191000.0
        )  # 48.82799834)
        # This will need checking about how SID2 is set
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(
            -9.999999848243207e33
        )  # 40500000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid2
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid2__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid2
def test_jui_rpwi_l1a_sid2__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(-1e31)
        assert test_array["Eu_i"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["Eu_i"].data[0][0] == pytest.approx(-2147483648)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid2
@pytest.mark.skip(reason="Quicklook not yet ready for SID 2.")
def test_jui_rpwi_l1a_sid2_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID3
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid3
def test_jui_rpwi_l1a_sid3_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID3)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid3
def test_jui_rpwi_l1a_sid3_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) in [9, 4, 8]  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] in [
            Time("2000-01-01 00:00:46.209668"),
            Time("2000-01-01 00:00:49.607418"),
            Time("2000-01-01 00:00:55.003582"),
            Time("2000-01-01 00:01:31.423855"),
        ]  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] in [
            Time("2000-01-01 00:05:18.209668"),
            Time("2000-01-01 00:02:31.607418"),
            Time("2000-01-01 00:04:53.003582"),
            Time("2000-01-01 00:05:29.423855"),
        ]


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid3
def test_jui_rpwi_l1a_sid3__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 255
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            84625.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(44591000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid3
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid3__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid3
def test_jui_rpwi_l1a_sid3__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(84.625)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] in [
            pytest.approx(2.5),
            pytest.approx(10496.0),
            pytest.approx(7.875),
            pytest.approx(2.75),
        ]
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid3
def test_jui_rpwi_l1a_sid3_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID4
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid4
def test_jui_rpwi_l1a_sid4_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID4)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid4
def test_jui_rpwi_l1a_sid4_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) in [3, 5]  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] in [
            Time("2000-01-01 00:00:57.245266"),
            Time("2000-01-01 00:01:00.872311"),
        ]  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] in [
            Time("2000-01-01 00:01:19.245266"),
            Time("2000-01-01 00:01:44.872311"),
        ]


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid4
def test_jui_rpwi_l1a_sid4__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 71
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            80000.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(2040000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid4
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid4__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid4
def test_jui_rpwi_l1a_sid4__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(80.0)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] in [
            pytest.approx(30.0),
            pytest.approx(37.0),
        ]
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid4
def test_jui_rpwi_l1a_sid4_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID20
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid20
def test_jui_rpwi_l1a_sid20_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID20)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid20
def test_jui_rpwi_l1a_sid20_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) in [41, 58]  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] in [
            Time("2000-01-01 00:00:46.245266"),
            Time("2000-01-01 00:00:50.872311"),
        ]  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] in [
            Time("2000-01-01 00:01:27.245266"),
            Time("2000-01-01 00:01:47.872311"),
        ]


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid20
def test_jui_rpwi_l1a_sid20__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 359
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            80000.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(2040000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid20
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid20__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid20
def test_jui_rpwi_l1a_sid20__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(80.0)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] in [
            pytest.approx(36.0),
            pytest.approx(47.0),
        ]
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid20
def test_jui_rpwi_l1a_sid20_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID5
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid5
def test_jui_rpwi_l1a_sid5_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID5)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid5
def test_jui_rpwi_l1a_sid5_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 5  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:00:44.661602"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:01:44.661602")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid5
def test_jui_rpwi_l1a_sid5__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 539
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            89250.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(10042250.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid5
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid5__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid5
def test_jui_rpwi_l1a_sid5__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(89.25)
        assert test_array["EE"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EE"].data[0][0] == pytest.approx(36864.0)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid5
def test_jui_rpwi_l1a_sid5_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID21
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid21
def test_jui_rpwi_l1a_sid21_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID21)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid21
def test_jui_rpwi_l1a_sid21_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 5  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:00:44.661602"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:01:44.661602")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid21
def test_jui_rpwi_l1a_sid21__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 4319
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            81156.25
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(10066531.2)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid21
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid21__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid21
def test_jui_rpwi_l1a_sid21__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(81.15625)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] == pytest.approx(16384.0)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid21
def test_jui_rpwi_l1a_sid21_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID6
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid6
def test_jui_rpwi_l1a_sid6_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID6)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid6
def test_jui_rpwi_l1a_sid6_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 9  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:26:25.873639"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:30:25.873639")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid6
def test_jui_rpwi_l1a_sid6__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 255
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            84625.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(44591000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid6
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid6__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid6
def test_jui_rpwi_l1a_sid6__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(84.625)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] == pytest.approx(2.5)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid6
def test_jui_rpwi_l1a_sid6_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID22
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid22
def test_jui_rpwi_l1a_sid22_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID22)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid22
def test_jui_rpwi_l1a_sid22_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 10  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:25:55.873639"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:30:25.873639")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid22
def test_jui_rpwi_l1a_sid22__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 255
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            84625.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(44591000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid22
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid22__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid22
def test_jui_rpwi_l1a_sid22__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(84.625)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] == pytest.approx(2.5)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid22
def test_jui_rpwi_l1a_sid22_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID7
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid7
def test_jui_rpwi_l1a_sid7_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID7)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid7
def test_jui_rpwi_l1a_sid7_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 1  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:00:47.873639"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:00:47.873639")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid7
def test_jui_rpwi_l1a_sid7__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 255
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            84625.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(44591000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid7
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid7__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid7
def test_jui_rpwi_l1a_sid7__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(84.625)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] == pytest.approx(2.5)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid7
def test_jui_rpwi_l1a_sid7_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# SID23
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid23
def test_jui_rpwi_l1a_sid23_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JuiceRPWIhfL1aCdfSID23)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid23
def test_jui_rpwi_l1a_sid23_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 1  # in [1, 3, 4, 5, 7, 8, 9, 10, 41, 58]
        assert data.times[0] == Time(
            "2000-01-01 00:00:47.873639"
        )  # "2000-01-01 00:00:46.245266")
        assert data.times[-1] == Time("2000-01-01 00:00:47.873639")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid23
def test_jui_rpwi_l1a_sid23__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 255
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(
            84625.0
        )  # 48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(44591000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid23
@pytest.mark.skip(reason="Sweeps not implemented for JUICE yet.")
def test_jui_rpwi_l1a_sid23__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], list)
        for i in range(6):
            print(i)
            print(sweep[2][i])
            assert isinstance(sweep[2][i], Quantity)
        assert len(sweep[2]) == 6
        # assert len(sweep[2][0]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid23
def test_jui_rpwi_l1a_sid23__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(84.625)
        assert test_array["EuEu"].attrs["units"] == "(raw)"  # "V**2 m**-2 Hz**-1"
        assert test_array["EuEu"].data[0][0] == pytest.approx(2.5)
        assert set(data.dataset_keys) == set(list(test_array.keys()))


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file_l1asid23
def test_jui_rpwi_l1a_sid23_quicklook(filepath):
    with Data(filepath=filepath) as data:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
