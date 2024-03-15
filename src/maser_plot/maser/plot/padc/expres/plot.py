# -*- coding: utf-8 -*-


"""
    EXPRES Simulation data reader


    .. code-block:: python

        from maser.data import Data
        expres = Data(
            filepath='<path>/expres_juno_jupiter_ganymede_jrm09_lossc-wid1deg_3kev_20211218_v11.cdf',
            source='Ganymede NORTH'
        )


"""


from maser.plot.base import CdfPlot

# from plot.base import CdfPlot

from abc import ABC
from typing import Union, List
from pathlib import Path
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

__all__ = ["ExpresCdfPlot"]


class ExpresCdfPlot(CdfPlot, ABC, dataset="expres"):
    """Base class for EXPRES datasets."""

    _dataset_keys = [
        "CML",
        "Polarization",
        "FC",
        "FP",
        "Theta",
        "ObsDistance",
        "ObsLatitude",
        "SrcFreqMax",
        "SrcFreqMaxCMI",
        "SrcLongitude",
        "VisibleSources"  # Not used in 'routine' simulations
        # 'Azimuth' # WIP
        # 'ObsLocalTime' # WIP
    ]

    def __init__(
        self,
        filepath: Path,
        source: Union[None, str] = None,
    ) -> None:
        self.source = source

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["FC", "FP", "Polarization", "Theta"],
        **kwargs,
    ) -> None:
        self._main_plot(
            keys=keys,
            db=[False, False, False, False],
            file_png=file_png,
            vmin=None,  # [-360, -10],
            vmax=None,  # [360, 10],
            **kwargs,
        )
