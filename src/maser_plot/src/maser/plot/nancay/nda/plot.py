# -*- coding: utf-8 -*-
from maser.plot.base import CdfPlot, FitsPlot

# from plot.base import CdfPlot, FitsPlot

from typing import Union, List
from pathlib import Path


class OrnNdaRoutineEdrCdfPlot(CdfPlot, dataset="orn_nda_routine_edr"):
    """ORN NDA Routine Jupiter dataset"""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["LL", "RR"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )


class OrnNdaRoutineJupEdrCdfPlot(
    OrnNdaRoutineEdrCdfPlot, dataset="orn_nda_routine_jup_edr"
):
    """ORN NDA Routine Jupiter dataset"""

    pass


class OrnNdaRoutineSunEdrCdfPlot(
    OrnNdaRoutineEdrCdfPlot, dataset="orn_nda_routine_sun_edr"
):
    """ORN NDA Routine Sun dataset"""

    pass


class OrnNdaNewRoutineEdrFitsPlot(FitsPlot, dataset="orn_nda_newroutine_edr"):
    """ORN NDA NewRoutine dataset"""

    pass


class OrnNdaNewRoutineSunEdrFitsPlot(
    OrnNdaNewRoutineEdrFitsPlot, dataset="orn_nda_newroutine_sun_edr"
):
    """ORN NDA NewRoutine Sun dataset"""

    def main_plot(self, file_png=None, keys: List[str] = ["LL", "RR"], **kwargs):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            vmin=[68, 68],
            vmax=[94, 94],
            db=[True, True],
            **kwargs,
        )


class OrnNdaNewRoutineJupEdrFitsPlot(
    OrnNdaNewRoutineEdrFitsPlot, dataset="orn_nda_newroutine_jup_edr"
):
    """ORN NDA NewRoutine Jupiter dataset"""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["LL", "RR"],
        **kwargs,
    ):
        self._main_plot(keys=keys, file_png=file_png, db=[True, True], **kwargs)


class OrnNdaNewRoutineTransitEdrFitsPlot(
    OrnNdaNewRoutineEdrFitsPlot, dataset="orn_nda_newroutine_transit_edr"
):
    """ORN NDA NewRoutine Radio Source Transit dataset"""

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["LL", "RR"],
        **kwargs,
    ):
        self._main_plot(keys=keys, file_png=file_png, db=[True, True], **kwargs)


class OrnNdaMefistoSunEdrFitsPlot(
    OrnNdaNewRoutineEdrFitsPlot, dataset="orn_nda_mefisto_sun_edr"
):
    """ORN NDA Mefisto Sun dataset"""

    def main_plot(self, file_png=None, keys: List[str] = ["LL", "RR"], **kwargs):
        self._main_plot(keys=keys, file_png=file_png, db=[True, True], **kwargs)
