#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS Data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "GPLv3"
__version__ = "1.1"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "29-JAN-2019"
__project__ = "MASER/PADC PDS"

__all__ = ["load_pds_from_label"]

from maser.data.pds.classes import PDSLabelDict
from maser.data.pds.const import PDS_OBJECT_CLASSES


def load_pds_from_label(file=None, label_dict=None, verbose=False, debug=False, **kwargs):

    if file is not None:
        label = PDSLabelDict(file, verbose=verbose, debug=debug)
    else:
        label = label_dict
    return PDS_OBJECT_CLASSES[label['DATA_SET_ID']](file, label_dict=label, verbose=verbose, debug=debug, **kwargs)