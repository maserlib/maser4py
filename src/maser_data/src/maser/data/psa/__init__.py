# -*- coding: utf-8 -*-

"""
Classes for PSA datasets.

.. list-table:: Dataset Table
   :widths: 20 20 20 20 10 10
   :header-rows: 1

   * - Observatory
     - Instrument
     - Repository
     - Dataset-id
     - Format
     - Requires
   * - MarsExpress
     - MARSIS
     - TBD
     - `MEX-M-MARSIS-3-RDR-AIS-_`
     - PDS3
     - N/A

"""

from .mex import (  # noqa: F401
    MexMMarsis3RdrAisV1Data,
    MexMMarsis3RdrAisExt1V1Data,
    MexMMarsis3RdrAisExt2V1Data,
    MexMMarsis3RdrAisExt3V1Data,
    MexMMarsis3RdrAisExt4V1Data,
    MexMMarsis3RdrAisExt5V1Data,
    MexMMarsis3RdrAisExt6V1Data,
    MexMMarsis3RdrAisV1Sweep,
)
