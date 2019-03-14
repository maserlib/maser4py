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

from pathlib import Path
from maser.data.pds.const import PDS_OBJECT_CLASSES


def load_pds_from_label(input_var, fmt_label_dict=None, verbose=False, debug=False, **kwargs):

    from maser.data.pds.classes import PDSLabelDict

    if isinstance(input_var, str):
        file = input_var
        label = PDSLabelDict(input_var, fmt_label_dict=fmt_label_dict, verbose=verbose, debug=debug)
    elif isinstance(input_var, Path):
        file = str(input_var)
        label = PDSLabelDict(file, fmt_label_dict=fmt_label_dict, verbose=verbose, debug=debug)
    elif isinstance(input_var, PDSLabelDict):
        label = input_var
        file = label.file
    else:
        raise TypeError()

    return PDS_OBJECT_CLASSES[label['DATA_SET_ID']](file, label_dict=label, verbose=verbose, debug=debug, **kwargs)
