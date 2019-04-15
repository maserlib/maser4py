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


def load_pds_from_label(label_path=None, label_dict=None, fmt_label_dict=None, verbose=False, debug=False, **kwargs):
    """This function loads the data associated with the provided PDS3 label file.

    One of the :code:`label_path` or :code:`label_dict` input parameter must be set, or a :code:`ValueError` is raised.
    
    * The :code:`label_path` must be either a simple path (:code:`str`) or a :code:`pathlib.Path` object. If the 
    parameter type is something else, a :code:`TypeError` is raised.
    * The :code:`label_dict` must be a :code:`PDSLabelDict` object. If the parameter type is something else, a 
    :code:`TypeError` is raised.
    
    The current list of available PDS3 data collections that have been tested are:
    {}

    :param label_path: Path to the label file (either a simple string or a pathlib.Path object)
    :param label_dict: PDSLabelDict object (already loaded from label file)
    :param fmt_label_dict: Dict with list of extra format label files (key=file name, value=file path)
    :param verbose: Verbose mode (default is False)
    :param debug: Debug mode (default is False)
    :param kwargs: any other keywords will be passed to the data object.
    :return: a PDSDataFromFile object.
    """.format("".join(['* {}\n'.format(item) for item in PDS_OBJECT_CLASSES.keys()]))

    from maser.data.pds.classes import PDSLabelDict

    label = dict()
    file = ''

    if label_path is not None or label_dict is not None:

        if isinstance(label_path, str):
            file = label_path
            label = PDSLabelDict(label_path, fmt_label_dict=fmt_label_dict, verbose=verbose, debug=debug)
        elif isinstance(label_path, Path):
            file = str(label_path)
            label = PDSLabelDict(file, fmt_label_dict=fmt_label_dict, verbose=verbose, debug=debug)
        elif isinstance(label_dict, PDSLabelDict):
            label = label_dict
            file = label.file
        else:
            TypeError()

        return PDS_OBJECT_CLASSES[label['DATA_SET_ID']](file, label_dict=label, verbose=verbose, debug=debug, **kwargs)

    else:

        raise ValueError()

