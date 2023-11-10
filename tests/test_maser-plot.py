# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.plot import Plot
from pathlib import Path
from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "jno_wav_cdr_lesia": [
        BASEDIR / "maser" / "juno" / "jno_wav_cdr_lesia_20170329_v02.cdf"
    ],
    "padc_bepi_sorbet": [
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_20211001_v00.cdf",
        BASEDIR
        / "bepi"
        / "sorbet"
        / "mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_20211002_v00.cdf",
    ],
}

# create a decorator to test each file in the list
for_each_test_file = pytest.mark.parametrize(
    "filepath", TEST_FILES["jno_wav_cdr_lesia"]
)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_main_plot(filepath):
    plot = Plot(filepath)
    ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
    plot.main_plot(ql_path_tmp)
    #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
    assert ql_path_tmp.is_file()
    ql_path_tmp.unlink()
