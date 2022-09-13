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

# -*- coding: utf-8 -*-
from .padc import (  # noqa: F401
    JnoWavLesiaL3aV02Data,
    CoRpwsHfrKronosN1Data,
    CoRpwsHfrKronosN2Data,
)

from .pds import (  # noqa: F401
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
    Vg1JPra4SummBrowse48secV1Data,
    Vg1SPra3RdrLowband6secV1Data,
    Vg2NPra2RdrHighrate60msV1Data,
    Vg2NPra3RdrLowband6secV1Data,
    CoVEJSSSRpws2RefdrWbrFullV1Data,
    CoVEJSSSRpws3RdrLrFullV1Data,
)
from .psa import MexMMarsis3RdrAisExt4V1Data  # noqa: F401

from .rpw import (  # noqa: F401
    RpwLfrSurvBp1,
)


if __name__ == "__main__":
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    print(type(data))
