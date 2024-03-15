# -*- coding: utf-8 -*-
from maser.plot.base import BinPlot

# from plot.base import BinPlot

from typing import List


class InterballAuroralPolradRspBinPlot(BinPlot, dataset="cdpp_int_aur_polrad_rspn2"):
    """Class for `cdpp_int_aur_polrad_rspn2` binary data"""

    def main_plot(self, file_png=None, keys: List[str] = ["EX", "EY", "EZ"], **kwargs):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            db=[True, True, True],
            **kwargs,
        )
