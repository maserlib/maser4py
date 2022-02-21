# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.data import CdfData, SrnNdaRoutineJupEdrCdfData
from pathlib import Path


BASEDIR = Path(__file__).resolve().parent / "data"


def test_cdf_dataset():
    data = Data(filepath="toto.txt", dataset="cdf")
    assert isinstance(data, CdfData)


def test_srn_nda_routine_jup_edr_dataset():
    data = Data(
        filepath=BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf"
    )
    assert isinstance(data, SrnNdaRoutineJupEdrCdfData)
