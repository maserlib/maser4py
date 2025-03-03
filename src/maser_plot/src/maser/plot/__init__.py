# -*- coding: utf-8 -*-
from .base import Plot
from pathlib import Path

from .cdpp import (  # noqa: F401
    WindWavesRad1L260sV2BinPlot,
    WindWavesRad1L2BinPlot,
    WindWavesRad2L260sV2BinPlot,
    WindWavesTnrL260sV2BinPlot,
    WindWavesTnrL3Bqt1mnBinPlot,
    WindWavesTnrL3NnBinPlot,
    WindWavesRad1L260sV1BinPlot,
    WindWavesRad2L260sV1BinPlot,
    WindWavesTnrL260sV1BinPlot,
    VikingV4nE5BinPlot,
    InterballAuroralPolradRspBinPlot,
    StereoAWavesL2HighResLfrBinPlot,
)
from .ecallisto import (  # noqa: F401
    ECallistoFitsPlot,
)
from .nancay import (  # noqa: F401
    OrnNdaRoutineJupEdrCdfPlot,
    OrnNdaRoutineSunEdrCdfPlot,
    OrnNdaNewRoutineJupEdrFitsPlot,
    OrnNdaNewRoutineSunEdrFitsPlot,
    OrnNdaNewRoutineTransitEdrFitsPlot,
    OrnNenufarBstFitsPlot,
)
from .padc import (  # noqa: F401
    JnoWavLesiaL3aV02Plot,
    CoRpwsHfrKronosN1Plot,
    CoRpwsHfrKronosN2Plot,
    StaWavLfrL3DfCdfPlot,
    StbWavLfrL3DfCdfPlot,
    StaWavHfrL3DfCdfPlot,
    StbWavHfrL3DfCdfPlot,
    WindWavesRad1L3DfV01Plot,
    WindWavesRad1L3DfV02Plot,
    SorbetCdfPlot,
)

from .pds import (  # noqa: F401
    Pds3Plot,
    Vg1JPra3RdrLowband6secV1Plot,
    Vg1JPra4SummBrowse48secV1Plot,
    Vg1SPra3RdrLowband6secV1Plot,
    Vg2JPra4SummBrowse48secV1Plot,
    Vg2NPra2RdrHighrate60msV1Plot,
    Vg2NPra3RdrLowband6secV1Plot,
    Vg2NPra4SummBrowse48secV1Plot,
    Vg2UPra3RdrLowband6secV1Plot,
    Vg2UPra4SummBrowse48secV1Plot,
    CoVEJSSSRpws2RefdrWbrFullV1Plot,
    CoVEJSSSRpws3RdrLrFullV1Plot,
)
from .psa import MexMMarsis3RdrAisExt4V1Plot  # noqa: F401

from .rpw import (  # noqa: F401
    RpwLfrSurvBp1Plot,
    RpwTnrSurvPlot,
    RpwHfrSurvPlot,
)

if __name__ == "__main__":
    Plot = Plot(filepath=Path("toto.txt"), dataset="cdf")
    print(type(Plot))
