# -*- coding: utf-8 -*-

"""
Classes for PADC datasets.

.. list-table:: Dataset Table
   :widths: 20 20 20 20 10 10
   :header-rows: 1

   * - Observatory
     - Instrument
     - Repository
     - Dataset-id
     - Format
     - Requires
   * - BepiColombo/MMO
     - SORBET
     - TBD
     - `mmo_pwi_sorbet_l1_`
     - CDF
     - `spacepy`
   * - Cassini
     - RPWS
     - TBD
     - `co_rpws_hfr_kronos`
     - Bin
     - N/A
   * - EXPRES
     - EXPRES
     - TBD
     - `expres`
     - CDF
     - `spacepy`
   * - Juno
     - WAVES
     - TBD
     - `jno_wav_cdr_lesia`
     - CDF
     - `spacepy`
   * - SolarOrbiter
     - RPW
     - TBD
     - `solo_L__rpw-___-_`
     - CDF
     - `spacepy`
   * - STEREO
     - WAVES
     - TBD
     - `st__l__wav`
     - Bin
     - N/A
   * - Wind
     - WAVES
     - TBD
     - `wi_wa__rad1_l3_`
     - CDF
     - `spacepy`

"""

from .juno import (  # noqa: F401
    JnoWavLesiaL3aV02Data,
)

from .cassini import (  # noqa: F401
    CoRpwsHfrKronosN1Data,
    CoRpwsHfrKronosN2Data,
)
from .stereo import (  # noqa: F401
    StaWavLfrL2Bin,
    StbWavLfrL2Bin,
    StaWavHfrL2Bin,
    StbWavHfrL2Bin,
    StaWavLfrL3DfCdf,
    StbWavLfrL3DfCdf,
    StaWavHfrL3DfCdf,
    StbWavHfrL3DfCdf,
)

from .expres import *  # noqa: F401, F403

from .wind import (  # noqa: F401
    WindWavesRad1L3AkrData,
    WindWavesRad1L3DfV01Data,
    WindWavesRad1L3DfV02Data,
)

from .bepi import (  # noqa: F401
    SorbetL1CdfTnr,
    SorbetL1CdfDbsc,
)

from .solo import (  # noqa: F401
    RpwHfrSurv,
    RpwTnrSurv,
    RpwLfrSurvBp1,
    RpwHfrL3Cdf,
    RpwTnrL3Cdf,
)

from .juice import (  # noqa: F401
    JuiceRPWIhfL1aCdfSID2,
    JuiceRPWIhfL1aCdfSID3,
    JuiceRPWIhfL1aCdfSID4,
    JuiceRPWIhfL1aCdfSID20,
    JuiceRPWIhfL1aCdfSID5,
    JuiceRPWIhfL1aCdfSID21,
    JuiceRPWIhfL1aCdfSID6,
    JuiceRPWIhfL1aCdfSID22,
    JuiceRPWIhfL1aCdfSID7,
    JuiceRPWIhfL1aCdfSID23,
    JuiceRPWIhfL1bCdf,
)

# from .bepi.sorbet import SorbetCdfData  # noqa: F401
