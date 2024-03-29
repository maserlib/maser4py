# -*- coding: utf-8 -*-
import xarray
from maser.data.pds.utils import PDSLabelDict
from .constants import BASEDIR
from maser.data import Data
from maser.data.pds import (
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
    Vg1SPra3RdrLowband6secV1Data,
    Vg2NPra3RdrLowband6secV1Data,
)
import pytest
from astropy.time import Time
from astropy.units import Quantity

TEST_FILES = {
    "vg1_j_pra_3_rdr_lowband_6sec_v1": [
        BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    ],
    "vg1_s_pra_3_rdr_lowband_6sec_v1": [
        BASEDIR / "pds" / "VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA.LBL"
    ],
    "vg2_n_pra_3_rdr_lowband_6sec_v1": [
        BASEDIR / "pds" / "VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1" / "VG2_NEP_PRA_6SEC.LBL"
    ],
}

# PDS TESTS


@pytest.mark.test_data_required
def test_pds_label_dict():
    label = PDSLabelDict(
        label_file=BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    )
    assert isinstance(label, PDSLabelDict)


@pytest.mark.test_data_required
def test_pds3_dataset():
    data = Data(
        filepath=TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"][0], dataset="pds3"
    )
    assert isinstance(data, Data)
    assert isinstance(data, Pds3Data)


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg1JPra3RdrLowband6secV1Data)


@pytest.mark.test_data_required
def test_vg1_s_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg1_s_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg1SPra3RdrLowband6secV1Data)


@pytest.mark.test_data_required
def test_vg2_n_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg2_n_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg2NPra3RdrLowband6secV1Data)


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset__access_mode_file():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        x = data.as_xarray()
        assert isinstance(x, xarray.Dataset)


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset__as_xarray():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, dict)


@pytest.mark.test_data_required
def test_vg_rdr_lowband_6sec_v1_dataset__times():
    for dataset in TEST_FILES.keys():
        for filepath in TEST_FILES[dataset]:
            data = Data(filepath=filepath)
            times = data.times
            assert isinstance(times, Time)
            assert len(times) == data._nsweep


@pytest.mark.test_data_required
def test_vg_rdr_lowband_6sec_v1_dataset__frequencies():
    for dataset in TEST_FILES.keys():
        for filepath in TEST_FILES[dataset]:
            data = Data(filepath=filepath)
            freqs = data.frequencies
            assert isinstance(freqs, Quantity)
            assert len(freqs) == 70
