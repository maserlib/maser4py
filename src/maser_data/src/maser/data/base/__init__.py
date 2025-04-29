# -*- coding: utf-8 -*-

"""
Base Classes for MASER-Data
===========================

Data object classes
-------------------

Defined in base.

* `Data` Class: The `Data` class is the base class to be used to load data with the MASER-Data module.
* `BinData` Class: Generic class for custom binary formatted data products.
* `CdfData` Class: Generic class for CDF formatted data products.
* `FitsData` Class: Generic class for FITS formatted data products.

Iterator classes
----------------

Defined in sweeps and records.

* `Sweeps` Class: Generic iterator class for sweep-based access.
* `Records` Class: Generic iterator class for record-based access.

Spectral classes
----------------

Defined in mixins.

* `RecordsOnly` Class: Generic class for time series datasets.
* `FixedFrequencies` Class: Generic class for datasets with fixed spectral sampling.
* `VariableFrequencies` Class: Generic class for datasets with variable spectral sampling.
"""

from .base import (  # noqa: F401
    Data,
    BinData,
    CdfData,
    FitsData,
)
from .mixins import (  # noqa: F401
    RecordsOnly,
    FixedFrequencies,
    VariableFrequencies,
)
from .sweeps import Sweeps  # noqa: F401
from .records import Records  # noqa: F401
