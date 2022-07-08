# -*- coding: utf-8 -*-

"""
Classes for datasets produced with instruments located at Nançay Radio Observatory (ORN). The collections are
distributed by CDN (Centre de Données de Nançay).

.. list-table:: Dataset Table
   :widths: 20 20 20 20 10 10
   :header-rows: 1

   * - Observatory
     - Telescope
     - Repository
     - Dataset-id
     - Format
     - Requires
   * - ORN
     - NDA
     - CDN
     - `srn_nda_routine_jup_edr`
     - CDF
     - `spacepy`
   * - ORN
     - NenuFAR
     - CDN
     - `srn_nenufar_bst`
     - FITS
     - `nenupy`

"""

from .nda import (  # noqa: F401
    SrnNdaRoutineJupEdrCdfData,
)
from .nenufar import (  # noqa: F401
    NenufarBstFitsData,
)
