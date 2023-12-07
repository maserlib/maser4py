# -*- coding: utf-8 -*-

"""Classes for e-Callisto datasets"""

from maser.plot.base import FitsPlot

# from plot.base import FitsPlot

from typing import Union, List
from pathlib import Path


class ECallistoFitsPlot(FitsPlot, dataset="ecallisto"):
    """Class for `ecallisto` FITS files."""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["Flux Density"],
        landscape: bool = True,
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            landscape=landscape,
            file_png=file_png,
            **kwargs,
        )
