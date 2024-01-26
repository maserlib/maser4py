# -*- coding: utf-8 -*-

"""Classes for Sorbet datasets"""

from maser.plot.base import CdfPlot

# from plot.base import CdfPlot

from typing import Union
from pathlib import Path


class SorbetCdfPlot(CdfPlot, dataset="mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_"):
    """Class for `sorbet` CDF files."""

    def main_plot(
        self, file_png: Union[str, Path, None] = None, landscape: bool = True, **kwargs
    ):
        self._main_plot(
            keys=["sorbet_WPT_spectra"],
            file_png=file_png,
            # db=[True,True],
            landscape=landscape,
            yscale="log",
            **kwargs,
        )
