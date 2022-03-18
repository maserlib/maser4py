# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit

from maser.data import Data
from maser.data.cdpp import (
    InterballAuroralPolradRspBinData,
    InterballAuroralPolradRspSweep,
)
from pathlib import Path
import pytest


BASEDIR = Path(__file__).resolve().parent / "data"

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
def test_int_aur_polrad_rsp_bin_dataset__sweeps__load_data_false():
    for filepath in TEST_FILES["cdpp_int_aur_polrad_rspn2"]:
        sweeps = Data(filepath=filepath, load_data=False).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, InterballAuroralPolradRspSweep)
        data_i = sweep.data
        assert data_i is None


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
    assert len(data_i["EZ"]) == 240
    assert header_i["CHANNELS"] == 1
    assert data_i["EX"] is None
    assert data_i["EY"] is None


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
