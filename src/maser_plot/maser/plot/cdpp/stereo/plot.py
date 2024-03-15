# -*- coding: utf-8 -*-
from typing import Union, List

from maser.plot.base import BinPlot

# from plot.base import BinPlot


class StereoWavesL2HighResBinPlot(BinPlot, dataset="cdpp_st__l2_wav_h_res"):
    """Placeholder class for `cdpp_stX_l2_wav_XXX` binary data."""

    def main_plot(self, file_png=None, keys: Union[List[str], None] = None, **kwargs):

        self.fields = ["agc1", "agc2", "auto1", "auto2", "crossr", "crossi"]
        self.units = ["ADU", "ADU", "ADU", "ADU", "ADU", "ADU"]
        if keys is None:
            keys = self.fields
        self._main_plot(
            keys=keys,
            file_png=file_png,
            y="frequency",
            vmin=[-150, -160, -150, -160, -1, -1],
            vmax=[-120, -130, -120, -130, 1, 1],
            db=[True, True, True, True, False, False],
            **kwargs,
        )


class StereoAWavesL2HighResLfrBinPlot(
    StereoWavesL2HighResBinPlot,
    dataset="cdpp_sta_l2_wav_h_res_lfr",
):
    """CDPP STEREO-A Waves LFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_sta_l2_wav_h_res_lfr`
    - Data format: Binary"""


class StereoAWavesL2HighResHfrBinPlot(
    StereoWavesL2HighResBinPlot,
    dataset="cdpp_sta_l2_wav_h_res_hfr",
):
    """CDPP STEREO-A Waves HFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_sta_l2_wav_h_res_hfr`
    - Data format: Binary"""


class StereoBWavesL2HighResLfrBinPlot(
    StereoWavesL2HighResBinPlot,
    dataset="cdpp_stb_l2_wav_h_res_lfr",
):
    """CDPP STEREO-B Waves LFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_stb_l2_wav_h_res_lfr`
    - Data format: Binary"""


class StereoBWavesL2HighResHfrBinPlot(
    StereoWavesL2HighResBinPlot,
    dataset="cdpp_stb_l2_wav_h_res_hfr",
):
    """CDPP STEREO-B Waves HFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_stb_l2_wav_h_res_hfr`
    - Data format: Binary"""
