# -*- coding: utf-8 -*-

"""
Classes for e-Callisto datasets.

.. list-table:: Dataset Table
   :widths: 20 20 20 20 10 10
   :header-rows: 1

   * - Observatory
     - Telescope
     - Repository
     - Dataset-id
     - Format
     - Requires
   * - Various
     - e-Callisto
     - e-Callisto
     - `ecallisto`
     - FITS
     - N/A

"""

from .data import (  # noqa: F401
    ECallistoFitsData,
)
