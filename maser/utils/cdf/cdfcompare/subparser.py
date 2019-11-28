#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module template."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os

# ________________ HEADER _________________________


# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def add_cdfcompare_subparser(subparser):
    """cdf.cdfcompare script program."""
    cdfcompare_parser = subparser.add_parser('cdf_compare', help='Compare 2 CDF files.')
    cdfcompare_parser.add_argument('cdf_filepath1', help="Input CDF file path 1")
    cdfcompare_parser.add_argument('cdf_filepath2', help="Input CDF file path 2")
    cdfcompare_parser.add_argument('--ignore_gatt', nargs="+",
                                   default=[],
                                   help="Global attributes to ignore")
    cdfcompare_parser.add_argument('--ignore_zvar', nargs="+",
                                   default=[],
                                   help="Global attributes to ignore")
    cdfcompare_parser.add_argument('--ignore_vatt', nargs="+",
                                   default=[],
                                   help="Global attributes to ignore")
    cdfcompare_parser.add_argument('--precision', nargs="+",
                                   default=[],
                                   help="zVariable precision settings")

    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)