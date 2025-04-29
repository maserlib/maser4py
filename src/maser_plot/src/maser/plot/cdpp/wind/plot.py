# -*- coding: utf-8 -*-
from typing import List
from maser.plot.base import BinPlot

# from plot.base import BinPlot


class WindWavesRad1L260sV2BinPlot(BinPlot, dataset="cdpp_wi_wa_rad1_l2_60s_v2"):
    """CDPP Wind Waves RAD1 Level 2 60s-Average (version 2) dataset

    - Observatory/Facility: WIND
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_wi_wa_rad1_l2_60s_v2`
    - Data format: Binary"""


class WindWavesL2BinPlot(BinPlot, dataset="cdpp_wi_wa_l2"):
    """Placeholder class for `cdpp_wi_wa_XXX_l2` binary data."""

    def main_plot(self, file_png=None, keys: List[str] = ["VSPAL", "VZPAL"], **kwargs):
        self._main_plot(
            file_png=file_png,
            keys=keys,
            **kwargs,
        )


class WindWavesRad1L2BinPlot(WindWavesL2BinPlot, dataset="cdpp_wi_wa_rad1_l2"):
    """Class for `cdpp_wi_wa_rad1_l2` binary data."""

    pass


class WindWavesRad2L260sV2BinPlot(BinPlot, dataset="cdpp_wi_wa_rad2_l2_60s_v2"):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL260sV2BinPlot(BinPlot, dataset="cdpp_wi_wa_tnr_l2_60s_v2"):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL3Bqt1mnBinPlot(BinPlot, dataset="cdpp_wi_wa_tnr_l3_bqt_1mn"):
    """Class for `cdpp_wi_wa_tnr_l3_bqt_1mn` data."""

    pass


class WindWavesTnrL3NnBinPlot(BinPlot, dataset="cdpp_wi_wa_tnr_l3_nn"):
    """Class for `cdpp_wi_wa_tnr_l3_nn` data."""

    pass


class WindWavesL260sV1BinPlot(BinPlot, dataset="cdpp_wi_wa___l2_60s_v1"):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    pass


class WindWavesRad1L260sV1BinPlot(
    WindWavesL260sV1BinPlot, dataset="cdpp_wi_wa_rad1_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    pass


class WindWavesRad2L260sV1BinPlot(
    WindWavesL260sV1BinPlot, dataset="cdpp_wi_wa_rad2_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v1` binary data"""

    pass


class WindWavesTnrL260sV1BinPlot(
    WindWavesL260sV1BinPlot, dataset="cdpp_wi_wa_tnr_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v1` binary data"""

    pass
