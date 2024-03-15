# -*- coding: utf-8 -*-
from maser.plot.base import CdfPlot

# from plot.base import CdfPlot
from typing import List


class WindWavesRad1L3AkrPlot(CdfPlot, dataset="wi_wa_rad1_l3-akr"):

    _dataset_keys = [
        "FLUX_DENSITY",
        "SNR",
    ]

    def main_plot(
        self, file_png=None, keys: List[str] = ["FLUX_DENSITY", "SNR"], **kwargs
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            db=[True, True],
            **kwargs,
        )


class WindWavesRad1L3DfV01Plot(CdfPlot, dataset="wi_wav_rad1_l3_df_v01"):

    _dataset_keys = [
        "FLUX",
        "ELEVATION",
        "AZIMUTH",
        "ANGULAR_RADIUS",
        "MODULATION",
    ]

    pass


class WindWavesRad1L3DfV02Plot(CdfPlot, dataset="wi_wav_rad1_l3_df_v02"):

    _dataset_keys = [
        "STOKES_I",
        "SWEEP",
        # "NUM",
        "WAVE_AZIMUTH_SRF",
        "WAVE_COLATITUDE_SRF",
        "SOURCE_SIZE",
        "QUALITY_FLAG",
        "MODULATION_RATE",
    ]

    def main_plot(
        self, file_png=None, keys: List[str] = ["SWEEP", "STOKES_I"], **kwargs
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            db=[True, True],
            **kwargs,
        )
