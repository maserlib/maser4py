# -*- coding: utf-8 -*-
from maser.plot.base import CdfPlot, BinPlot

# from plot.base import CdfPlot, BinPlot
from typing import List


class StWavL2BinPlot(BinPlot, dataset="st__l2_wav"):
    pass


class StaWavLfrL2BinPlot(StWavL2BinPlot, dataset="sta_l2_wav_lfr"):
    pass


class StbWavLfrL2BinPlot(StWavL2BinPlot, dataset="stb_l2_wav_lfr"):
    pass


class StaWavHfrL2BinPlot(StWavL2BinPlot, dataset="sta_l2_wav_hfr"):
    pass


class StbWavHfrL2BinPlot(StWavL2BinPlot, dataset="stb_l2_wav_hfr"):
    pass


class StWavL3CdfPlot(CdfPlot, dataset="st__l3_wav"):
    def main_plot(
        self, file_png=None, keys: List[str] = ["PSD_FLUX", "STOKES_I"], **kwargs
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            db=[True, True],
            **kwargs,
        )


class StaWavLfrL3DfCdfPlot(StWavL3CdfPlot, dataset="sta_l3_wav_lfr"):
    """PADC/MASER STEREO-A Waves LFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves/LFR
    - Repository: PADC/MASER
    - Dataset-id: `sta_l3_wav_lfr`
    - Data format: CDF"""

    pass


class StbWavLfrL3DfCdfPlot(StWavL3CdfPlot, dataset="stb_l3_wav_lfr"):
    """PADC/MASER STEREO-B Waves LFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves/LFR
    - Repository: PADC/MASER
    - Dataset-id: `stb_l3_wav_lfr`
    - Data format: CDF"""

    pass


class StaWavHfrL3DfCdfPlot(StWavL3CdfPlot, dataset="sta_l3_wav_hfr"):
    """PADC/MASER STEREO-A Waves HFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves/HFR
    - Repository: PADC/MASER
    - Dataset-id: `sta_l3_wav_hfr`
    - Data format: CDF"""

    pass


class StbWavHfrL3DfCdfPlot(StWavL3CdfPlot, dataset="stb_l3_wav_hfr"):
    """PADC/MASER STEREO-B Waves HFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves/HFR
    - Repository: PADC/MASER
    - Dataset-id: `stb_l3_wav_hfr`
    - Data format: CDF"""

    pass
