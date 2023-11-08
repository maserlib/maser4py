# -*- coding: utf-8 -*-
from maser.plot.base import Plot

# from plot.base import Plot


class Pds3Plot(Plot, dataset="pds3"):

    pass


class Pds3DataTablePlot(Pds3Plot, dataset="pds3-table"):

    pass


class Pds3DataTimeSeriesPlot(Pds3Plot, dataset="pds3-time-series"):

    pass
