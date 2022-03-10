# -*- coding: utf-8 -*-
from maser.data.pds.utils import PDSLabelDict
from pathlib import Path
import pytest

BASEDIR = Path(__file__).resolve().parent / "data"


@pytest.mark.test_data_required
def test_pds_label_dict():
    label = PDSLabelDict(
        label_file=BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    )
    assert isinstance(label, PDSLabelDict)
