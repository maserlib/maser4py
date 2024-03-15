# -*- coding: utf-8 -*-

"""Classes for e-Callisto datasets"""

from maser.plot.base import CdfPlot

# from plot.base import FitsPlot

from typing import Union, List
from pathlib import Path


class RpwLfrSurvBp1Plot(CdfPlot, dataset="solo_L2_rpw-lfr-surv-bp1"):
    """Class for `RPW - LFR - SurvBP1` plot."""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = [
            "PB",
            "PE",
            "DOP",
            "ELLIP",
            "SX_REA",
            "DELTA_TIMES",
            "MODE_NB",
        ],
        db=[True, True, False, False, True, False, False],
        vmax=[-50, -60, 1, 1, 50, 0.2 * 10 ** (-8), 3],
        vmin=[-100, -130, 0, 0, -50, 0 * 10 ** (-8), 0],
        multiple_mode=0,
        **kwargs,
    ):
        if multiple_mode == 1:
            selection = {
                "select_key": ["MODE_NB", "MODE_NB"],
                "select_value": [1, 2],
                "select_dim": ["frequency", "frequency"],
                "select_how": ["all", "all"],
            }
        else:
            selection = None
        self._main_plot(
            keys=keys,
            file_png=file_png,
            db=db,
            # vmin=[0.008,0.006],
            vmax=vmax,
            vmin=vmin,
            # vmax=[0.009,0.007],
            iter_on_selection=selection,
            **kwargs,
        )


class RpwTnrSurvPlot(CdfPlot, dataset="solo_L2_rpw-tnr-surv"):
    """Class for `RPW - TNR - Surv` plot."""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = [
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "DELTA_TIMES",
        ],
        db: List[bool] = [True, True, False],
        vmin: List[Union[float, None]] = [None, None, -2e-5],
        vmax: List[Union[float, None]] = [None, None, 2e-5],
        yscale: str = "log",
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            db=db,
            vmin=vmin,
            vmax=vmax,
            yscale=yscale,
            **kwargs,
        )


class RpwHfrSurvPlot(CdfPlot, dataset="solo_L2_rpw-hfr-surv"):
    """Class for `RPW - HFR - Surv` plot."""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = [
            "VOLTAGE_SPECTRAL_POWER",
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "DELTA_TIMES",
            "FREQ_INDICES",
        ],
        db: List[bool] = [True, True, True, False, False],
        **kwargs,
    ):
        self._main_plot(keys=keys, file_png=file_png, db=db, **kwargs)
