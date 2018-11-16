#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to define classes for the NenuFAR (New Extension in Nançay Upgrading loFAR) datasets at Obs-Nancay.
@author: B.Cecconi(LESIA)

BST (Beam Statistic): Spectrum for the whole array (digital phasing).
SST (Spectrum Statistic): Spectrum per mini-array.
XST (Cross Statistic): Cross-correlation between mini-arrays.
"""

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "16-OCT-2017"
__version__ = "0.01"
__project__ = "MASER/SRN/NenuFAR"

__all__ = ["NenuFARBSTDataFromFile", "NenuFARSSTDataFromFile", "NenuFARDataECube"]

import os
from astropy.io import fits
from maser.data.data import MaserDataFromFileFITS, MaserData, MaserDataSweep


class NenuFARBSTSweep(MaserDataSweep):
    pass


class NenuFARBSTBeam(MaserData):
    pass


class NenuFARDataFromFile(MaserDataFromFileFITS):

    def __init__(self, file, verbose=True, debug=False):
        MaserDataFromFileFITS.__init__(self, file, verbose=verbose, debug=debug)
        self.check_file()
        self.header = fits.getheader(self.file)
        self.data = []

    def check_file(self):
        """
        Check if it is a proper NenuFAR file
        """
        if os.path.isfile(self.file):
            try:
                header = fits.getheader(self.file)
                if header['INSTRUME'] != 'NenuFar':
                    raise Exception('{} is not a NenuFAR data file'.format(self.file))
                else:
                    return
            except:
                raise Exception('{} must be a FITS file.'.format(self.file))
        else:
            raise IOError('NenuFAR {} not found'.format(self.file))

    def get_freq(self):
        """
        Read and return frequency properties
        """

        freqs = fits.getdata(self.file, ext=4)['freqList'][0]
        mfreq = freqs > 0.
        freqs = freqs[mfreq]

        return freqs, mfreq


class NenuFARBSTDataFromFile(NenuFARDataFromFile):

    def __init__(self, file, verbose=True, debug=False):
        NenuFARDataFromFile.__init__(self, file, verbose=verbose, debug=debug)
        self.name = "SRN/NenuFAR BST Dataset"


class NenuFARSSTDataFromFile(NenuFARDataFromFile):

    def __init__(self, file, verbose=True, debug=False):
        NenuFARDataFromFile.__init__(self, file, verbose=verbose, debug=debug)
        self.name = "SRN/NenuFAR SST Dataset"


class NenuFARXSTDataFromFile(NenuFARDataFromFile):
    def __init__(self, file, verbose=True, debug=False):
        NenuFARDataFromFile.__init__(self, file, verbose=verbose, debug=debug)
        self.name = "SRN/NenuFAR XST Dataset"

