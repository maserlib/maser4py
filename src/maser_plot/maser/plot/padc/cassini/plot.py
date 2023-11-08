# -*- coding: utf-8 -*-
from typing import List

from maser.plot.base import BinPlot

# from plot.base import BinPlot

import math


class CoRpwsHfrKronosPlot(BinPlot, dataset="co_rpws_hfr_kronos"):

    pass


class CoRpwsHfrKronosN1Plot(CoRpwsHfrKronosPlot, dataset="co_rpws_hfr_kronos_n1"):
    def main_plot(
        self,
        file_png=None,
        keys: List[str] = ["agc1", "auto1", "agc2", "auto2", "cross1", "cross2"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            vmax=[127, 191, 127, 191, 255, 255],
            vmin=[0, 128, 0, 128, -255, -255],
            **kwargs,
        )


class CoRpwsHfrKronosN2Plot(CoRpwsHfrKronosPlot, dataset="co_rpws_hfr_kronos_n2"):
    def main_plot(
        self,
        file_png=None,
        keys: List[str] = ["autoX", "autoZ", "crossR", "crossI"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            db=[True, True, False, False],
            file_png=file_png,
            y="frequency",
            yscale="log",
            **kwargs,
        )


class CoRpwsHfrKronosN3Plot(CoRpwsHfrKronosPlot, dataset="co_rpws_hfr_kronos_n3"):

    pass


class CoRpwsHfrKronosN3ePlot(CoRpwsHfrKronosN3Plot, dataset="co_rpws_hfr_kronos_n3e"):
    def main_plot(
        self,
        file_png=None,
        keys: List[str] = ["s", "v", "th", "ph", "snx", "snz"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            db=[True, False, False, False, True, True],
            file_png=file_png,
            y="frequency",
            yscale="log",
            vmin=[-160, -1, 0, -math.pi, 10, 10],
            vmax=[-120, 1, math.pi, math.pi, 40, 40],
            **kwargs,
        )


class CoRpwsHfrKronosN3dPlot(CoRpwsHfrKronosN3Plot, dataset="co_rpws_hfr_kronos_n3d"):
    def main_plot(
        self,
        file_png=None,
        keys: List[str] = ["s", "q", "u", "v", "snx", "snz"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            db=[True, False, False, False, True, True],
            file_png=file_png,
            y="frequency",
            yscale="log",
            vmin=[-160, -1, -1, -1, 10, 10],
            vmax=[-120, 1, 1, 1, 40, 40],
            **kwargs,
        )
