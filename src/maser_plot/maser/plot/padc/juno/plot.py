# -*- coding: utf-8 -*-
from maser.plot.base import CdfPlot

# from plot.base import CdfPlot
from typing import Union, List
from pathlib import Path


class JnoWavLesiaL3aV02Plot(CdfPlot, dataset="jno_wav_cdr_lesia"):

    _dataset_keys = ["INTENSITY", "BACKGROUND", "INTENSITY_BG_COR"]

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["INTENSITY", "BACKGROUND", "INTENSITY_BG_COR"],
        db: List[bool] = [True, True, True],
        # vmin: List[float] = [-137,-137, 0, -137],
        # vmax: List[float] = [-71,-71, 7e-8, -71],
        vmin_quantile: List[float] = [0.35, 0.35, 0.35],
        vmax_quantile: List[float] = [0.95, 0.95, 0.95],
        yscale: str = "log",
        calibrate: bool = True,
        landscape: bool = False,
        **kwargs,
    ):

        if calibrate:
            force_new_units = []
            force_new_keyname = []
            f = 1.0 / 377.0  # in Ohm - from Louis et al. 2021
            data_factor = []
            if "INTENSITY" in keys:
                force_new_units.append("W m**-2 Hz**-1")
                force_new_keyname.append("FLUX_DENSITY")
                data_factor.append(f)
            if "BACKGROUND" in keys:
                force_new_units.append("W m**-2 Hz**-1")
                force_new_keyname.append("BACKGROUND")
                data_factor.append(f)
            if "INTENSITY_BG_COR" in keys:
                force_new_units.append("W m**-2 Hz**-1")
                force_new_keyname.append("FLUX_DENSITY_BG_COR")
                data_factor.append(f)
            # force_new_units = ["W m**-2 Hz**-1", "W m**-2 Hz**-1", "W m**-2 Hz**-1"]
            # force_new_keyname = ["FLUX DENSITY", "BACKGROUND", "FLUX DENSITY_BG_COR"]
            # data_factor = [f, f, f]
        else:
            force_new_units = None
            force_new_keyname = None
            data_factor = None

        self._main_plot(
            keys=keys,
            file_png=file_png,
            db=db,
            vmin_quantile=vmin_quantile,
            vmax_quantile=vmax_quantile,
            yscale=yscale,
            force_new_units=force_new_units,
            force_new_keyname=force_new_keyname,
            data_factor=data_factor,
            landscape=landscape,
            **kwargs,
        )
