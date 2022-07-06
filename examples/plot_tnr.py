# -*- coding: utf-8 -*-
import pathlib
from maser.data import Data

ROOT_DIR = pathlib.Path(__file__).parent.parent

tnr_data_path = ROOT_DIR / "tests" / "solo_L2_rpw-tnr-surv_20210701_V01.cdf"


def plot_tnr():
    print(tnr_data_path)
    data = Data(tnr_data_path)
    data._init_
    print(data.frequencies()["A"])
    data.plot_tnr_data_for_quicklook_SonnyVersion()


if __name__ == "__main__":
    plot_tnr()


