#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS Data
@author: B.Cecconi(LESIA)
"""

import struct
import datetime
import os
from maser.data.data import *
from maser.data.pds.ppi.voyager import *

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "GPLv3"
__version__ = "1.0b0"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "11-SEP-2017"
__project__ = "MASER/PADC"

__all__ = ["extract_pds_label", "PDSData"]


def extract_pds_label(file):

    label = dict()

    with open(file, 'r') as f:
        while True:
            line = f.readline().strip()
            if line == "END":
                break
            elif line.startswith('/*'):
                continue
            elif '=' in line:
                kv = line.split('=')
                label[kv[0].strip()] = kv[1].strip()

    return label