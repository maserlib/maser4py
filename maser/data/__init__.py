# -*- coding: utf-8 -*-
from .base import Data
from pathlib import Path

from .cdpp import (  # noqa: F401
    WindWavesRad1L260sV2BinData,
    WindWavesRad1L2BinData,
    WindWavesRad2L260sV2BinData,
    WindWavesTnrL260sV2BinData,
    WindWavesTnrL3Bqt1mnBinData,
    WindWavesTnrL3NnBinData,
    WindWavesRad1L260sV1BinData,
    WindWavesRad2L260sV1BinData,
    WindWavesTnrL260sV1BinData,
    VikingV4nE5BinData,
    InterballAuroralPolradRspBinData,
)
from .ecallisto import (  # noqa: F401
    ECallistoFitsData,
)
from .nancay import (  # noqa: F401
    SrnNdaRoutineJupEdrCdfData,
    NenufarBstFitsData,
)
from .pds import (  # noqa: F401
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
)

from .rpw import (  # noqa: F401
    RpwLfrSurvBp1,
)


if __name__ == "__main__":
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    print(type(data))
