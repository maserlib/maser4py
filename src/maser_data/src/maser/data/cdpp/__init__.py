# -*- coding: utf-8 -*-

"""
Classes for CDPP datasets.

.. list-table:: Dataset Table
   :widths: 20 20 20 20 10 10
   :header-rows: 1

   * - Observatory
     - Instrument
     - Repository
     - Dataset-id
     - Format
     - Requires
   * - Wind
     - WAVES
     - TBD
     - `cdpp_wi_wa_`
     - Bin
     - N/A
   * - Interball
     - Aurora
     - TBD
     - `cdpp_int_aur_polrad_rspn2`
     - Bin
     - N/A
   * - STEREO
     - WAVES
     - TBD
     - `cdpp_st__l2_wav_`
     - Bin
     - N/A
   * - Viking
     - TBD
     - TBD
     - `cdpp_viking_v4n_e5`
     - Bin
     - N/A

"""

from .wind import (  # noqa: F401
    WindWavesRad1L260sV2BinData,
    WindWavesRad1L260sV1BinData,
    WindWavesRad2L260sV1BinData,
    WindWavesTnrL260sV1BinData,
    WindWavesRad1L2BinData,
    WindWavesTnrL3NnBinData,
    WindWavesTnrL260sV2BinData,
    WindWavesRad2L260sV2BinData,
    WindWavesTnrL3Bqt1mnBinData,
)
from .wind import (  # noqa: F401
    WindWavesL260sSweeps,
    WindWavesL2HighResSweeps,
    WindWaves60sSweeps,
)
from .wind import (  # noqa: F401
    WindWavesTnrL3Bqt1mnRecords,
)
from .viking import (  # noqa: F401
    VikingV4nE5BinData,
)
from .interball import (  # noqa: F401
    InterballAuroralPolradRspBinData,
)
from .interball import (  # noqa: F401
    InterballAuroralPolradRspSweeps,
    InterballAuroralPolradRspSweep,
)
from .interball import (  # noqa: F401
    InterballAuroralPolradRspRecords,
    InterballAuroralPolradRspRecord,
)
from .stereo import (  # noqa: F401
    StereoAWavesL2HighResLfrBinData,
    StereoAWavesL2HighResHfrBinData,
    StereoBWavesL2HighResLfrBinData,
    StereoBWavesL2HighResHfrBinData,
)
