# -*- coding: utf-8 -*-
from maser.data.pds.utils import PDSLabelDict
from pathlib import Path

from maser.data import Data
from maser.data.pds import (
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
)
import pytest

BASEDIR = Path(__file__).resolve().parent / "data"

TEST_FILES = {
    "vg1_j_pra_3_rdr_lowband_6sec_v1": [
        BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    ],
}

# PDS TESTS


@pytest.mark.test_data_required
def test_pds_label_dict():
    label = PDSLabelDict(
        label_file=BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    )
    assert isinstance(label, PDSLabelDict)


def test_pds3_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="pds3")
    assert isinstance(data, Data)
    assert isinstance(data, Pds3Data)


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg1JPra3RdrLowband6secV1Data)


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset__access_mode_file():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, dict)
