#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module containing the cdfvalidator subparser."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os

__all__ = ["add_cdfvalidator_subparser"]

# ________________ HEADER _________________________




# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def add_cdfvalidator_subparser(subparser):
    """cdf.validator script program."""

    valparser = subparser.add_parser('cdf_validator',
        help='Validate a CDF format file')
    valparser.add_argument('cdf_file', nargs=1,
                        default=[None],
                        help='Path of the CDF format file to validate')
    valparser.add_argument('-m', '--model-file', nargs=1,
                        default=[None],
                        help='Path to the model file in JSON format')
    valparser.add_argument('-c', '--cdfvalidate-bin', nargs=1,
                        default=[None],
                        help='Path of the cdfvalidate NASA CDF tool executable')
    valparser.add_argument('-I', '--istp', action='store_true',
                        help='Check the ISTP guidelines compliance')
    valparser.add_argument('-C', '--run-cdfvalidate', action='store_true',
                        help='Run the cdfvalidate NASA CDF tool')


    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)
