# -*- coding: utf-8 -*-

"""
Base Classes for MASER-Plot
===========================

Plot object classes
-------------------

* `Plot` Class: The `Plot` class is the base class to be used to plot Plot with the MASER-Plot module.
* `BinPlot` Class: Generic class for custom binary formatted Plot products.
* `CdfPlot` Class: Generic class for CDF formatted Plot products.
* `FitsPlot` Class: Generic class for FITS formatted Plot products.

"""


from .base import (  # noqa: F401
    Plot,
    BinPlot,
    CdfPlot,
    FitsPlot,
)
