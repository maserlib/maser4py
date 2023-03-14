# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data.cdpp import (
    InterballAuroralPolradRspBinData,
    InterballAuroralPolradRspSweep,
    InterballAuroralPolradRspRecord,
)
import pytest
from pathlib import Path


TEST_FILES = {
    "cdpp_int_aur_polrad_rspn2": [
        BASEDIR / "cdpp" / "interball" / "POLR_RSPN2_19971116",
        BASEDIR / "cdpp" / "interball" / "POLR_RSPN2_19990126",
    ],
}


# CDPP/INTERBALL TESTS ==== int_aur_polrad_rst
@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset():
    for filepath in TEST_FILES["cdpp_int_aur_polrad_rspn2"]:
        data = Data(filepath=filepath)
        assert isinstance(data, InterballAuroralPolradRspBinData)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__file_size():
    file_sizes = [10038036, 1073108]
    for filepath, file_size in zip(TEST_FILES["cdpp_int_aur_polrad_rspn2"], file_sizes):
        data = Data(filepath=filepath)
        assert data.file_size.value == file_size


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__sweeps_for_loop():
    for filepath in TEST_FILES["cdpp_int_aur_polrad_rspn2"]:
        for sweep in Data(filepath=filepath):
            assert isinstance(sweep, InterballAuroralPolradRspSweep)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__sweeps_next__file0():
    header_result = {
        "CCSDS_PREAMBLE": 76,
        "CCSDS_JULIAN_DAY_B1": 0,
        "CCSDS_JULIAN_DAY_B2": 68,
        "CCSDS_JULIAN_DAY_B3": 78,
        "CCSDS_MILLISECONDS_OF_DAY_B0": 0,
        "CCSDS_MILLISECONDS_OF_DAY_B1": 0,
        "CCSDS_MILLISECONDS_OF_DAY_B2": 21,
        "CCSDS_MILLISECONDS_OF_DAY_B3": 41,
        "ATTENUATION": 0,
        "CHANNELS": 1,
        "SWEEP_DURATION": 3.249000072479248,
        "STEPS": 240,
        "SESSION_NAME": "73204S21",
        "FIRST_FREQ": 987.1360473632812,
        "CCSDS_CDS_LEVEL2_EPOCH": Time("1950-01-01 00:00:00.000"),
        "P_Field": 56,
        "T_Field": bytearray(b"\x00DN\x00\x00\x15)"),
        "SWEEP_ID": 0,
    }
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    sweeps = Data(filepath=filepath).sweeps
    sweep = next(sweeps)
    assert isinstance(sweep, InterballAuroralPolradRspSweep)
    header_i = sweep.header
    data_i = sweep.data
    assert header_i == header_result
    assert list(data_i.keys()) == ["EX", "EY", "EZ"]
    assert len(data_i["EY"]) == 240
    assert header_i["CHANNELS"] == 1
    assert data_i["EX"] is None
    assert data_i["EZ"] is None


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__sweeps_next__file1():
    header_result = {
        "CCSDS_PREAMBLE": 76,
        "CCSDS_JULIAN_DAY_B1": 0,
        "CCSDS_JULIAN_DAY_B2": 70,
        "CCSDS_JULIAN_DAY_B3": 2,
        "CCSDS_MILLISECONDS_OF_DAY_B0": 1,
        "CCSDS_MILLISECONDS_OF_DAY_B1": 24,
        "CCSDS_MILLISECONDS_OF_DAY_B2": 122,
        "CCSDS_MILLISECONDS_OF_DAY_B3": 82,
        "ATTENUATION": 0,
        "CHANNELS": 3,
        "SWEEP_DURATION": 6.5,
        "STEPS": 240,
        "SESSION_NAME": "90262S21",
        "FIRST_FREQ": 987.1360473632812,
        "CCSDS_CDS_LEVEL2_EPOCH": Time("1950-01-01 00:00:00.000"),
        "P_Field": 56,
        "T_Field": bytearray(b"\x00F\x02\x01\x18zR"),
        "SWEEP_ID": 0,
    }
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][1]
    sweeps = Data(filepath=filepath).sweeps
    sweep = next(sweeps)
    assert isinstance(sweep, InterballAuroralPolradRspSweep)
    header_i = sweep.header
    data_i = sweep.data
    assert header_i == header_result
    assert list(data_i.keys()) == ["EX", "EY", "EZ"]
    assert len(data_i["EZ"]) == 240
    assert header_i["CHANNELS"] == 3
    assert len(data_i["EX"]) == 240
    assert len(data_i["EY"]) == 240


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__times():
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    data = Data(filepath=filepath)
    assert data._times is None
    assert isinstance(data.times, Time)
    assert data._times is not None
    assert len(data.times) == 4959
    assert data.times[0].jd == pytest.approx(Time("1997-11-15 23:59:34.417").jd)
    assert data.times[-1].jd == pytest.approx(Time("1997-11-16 23:31:26.418").jd)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__frequencies():
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    data = Data(filepath=filepath)
    assert data._frequencies is None
    assert isinstance(data.frequencies, Quantity)
    assert data._frequencies is not None
    assert len(data.frequencies) == 240
    assert data.frequencies.unit == Unit("kHz")
    assert data.frequencies[0].value == pytest.approx(983.04)
    assert data.frequencies[-1].value == pytest.approx(4.096)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__session_file0():
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    data = Data(filepath=filepath)
    sweeps = data.sweeps
    header_i = next(sweeps).header
    session = data.decode_session_name(header_i["SESSION_NAME"])
    assert isinstance(session, dict)
    assert session == {
        "YEAR": 1997,
        "DOY": 320,
        "SUB_SESSION_NB": 4,
        "TELEMETRY_TYPE": "SSNI",
        "TELEMETRY_MODE": "MEMORY",
        "STATION_CODE": "EVPATORIA",
    }


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__session_file1():
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][1]
    data = Data(filepath=filepath)
    sweeps = data.sweeps
    header_i = next(sweeps).header
    session = data.decode_session_name(header_i["SESSION_NAME"])
    assert isinstance(session, dict)
    assert session == {
        "YEAR": 1999,
        "DOY": 26,
        "SUB_SESSION_NB": 2,
        "TELEMETRY_TYPE": "SSNI",
        "TELEMETRY_MODE": "MEMORY",
        "STATION_CODE": "EVPATORIA",
    }


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__records_next__file0():
    header_result = {
        "CCSDS_PREAMBLE": 76,
        "CCSDS_JULIAN_DAY_B1": 0,
        "CCSDS_JULIAN_DAY_B2": 68,
        "CCSDS_JULIAN_DAY_B3": 78,
        "CCSDS_MILLISECONDS_OF_DAY_B0": 0,
        "CCSDS_MILLISECONDS_OF_DAY_B1": 0,
        "CCSDS_MILLISECONDS_OF_DAY_B2": 21,
        "CCSDS_MILLISECONDS_OF_DAY_B3": 41,
        "ATTENUATION": 0,
        "CHANNELS": 1,
        "SWEEP_DURATION": 3.249000072479248,
        "STEPS": 240,
        "SESSION_NAME": "73204S21",
        "FIRST_FREQ": 987.1360473632812,
        "CCSDS_CDS_LEVEL2_EPOCH": Time("1950-01-01 00:00:00.000"),
        "P_Field": 56,
        "T_Field": bytearray(b"\x00DN\x00\x00\x15)"),
        "SWEEP_ID": 0,
    }
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    records = Data(filepath=filepath).records
    record = next(records)
    assert isinstance(record, InterballAuroralPolradRspRecord)
    header_i = record.header
    data_i = record.data
    assert header_i.keys() == header_result.keys()
    assert record.time.jd == pytest.approx(Time("1997-11-15 23:59:34.417").jd)
    assert record.frequency.unit == Unit("kHz")
    assert record.frequency.value == pytest.approx(983.04)
    assert list(data_i.keys()) == ["EX", "EY", "EZ"]
    record = next(records)
    assert record.time.jd == pytest.approx(Time("1997-11-15 23:59:34.417").jd)
    assert record.frequency.value == pytest.approx(978.944)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__records_for_loop__file0():
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    counter = 0
    for record in Data(filepath=filepath).records:
        assert isinstance(record, InterballAuroralPolradRspRecord)
        if counter == 0:
            assert record.time == Time("1997-11-15 23:59:34.417")
            assert record.frequency.value == pytest.approx(983.04)
        if counter == 1:
            assert record.time == Time("1997-11-15 23:59:34.417")
            assert record.frequency.value == pytest.approx(978.944)
        if counter == 240:
            assert record.time == Time("1997-11-15 23:59:41.417")
            assert record.frequency.value == pytest.approx(983.04)
        if counter == 241:
            assert record.time == Time("1997-11-15 23:59:41.417")
            assert record.frequency.value == pytest.approx(978.944)
        assert record.header["SWEEP_ID"] == counter // 240
        counter += 1
        if counter > 300:
            break


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__epncore():
    filepath = TEST_FILES["cdpp_int_aur_polrad_rspn2"][0]
    data = Data(filepath=filepath)
    md = data.epncore()
    expected_md = {
        "access_estsize": 9803,
        "access_format": "application/octet-stream",
        "file_name": "POLR_RSPN2_19971116",
        "granule_gid": "cdpp_int_aur_polrad_rspn2",
        "granule_uid": "cdpp_int_aur_polrad_rspn2:POLR_RSPN2_19971116",
        "time_max": 2450769.480166875,
        "time_min": 2450768.4997039004,
        "time_sampling_step_max": pytest.approx(32783.499999),
        "time_sampling_step_min": pytest.approx(4.2509999),
        "instrument_host_name": "interball-auroral",
        "instrument_name": "polrad",
        "target_name": "Earth",
        "target_class": "planet",
        "target_region": "magnetosphere",
        "feature_name": "AKR#Auroral Kilometric Radiation",
        "dataproduct_type": "ds",
        "spectral_range_min": pytest.approx(4096.0),
        "spectral_range_max": pytest.approx(983040.0),
        "publisher": "CNES/CDPP",
    }
    assert isinstance(md, dict)
    assert md == expected_md


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__as_xarray():
    for filepath in TEST_FILES["cdpp_int_aur_polrad_rspn2"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, dict)
        assert set(xr.keys()) == {"EX", "EY", "EZ"}
        assert xr["EY"].shape == (240, 367)
        assert xr["EY"].attrs["units"] == "W m^-2 Hz^-1"


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__quicklook():
    for filepath in TEST_FILES["cdpp_int_aur_polrad_rspn2"]:
        ql_path = BASEDIR.parent / "quicklook" / "cdpp" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        data.quicklook(ql_path_tmp)
        assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        ql_path_tmp.unlink()
