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
    cdfcompare_parser = subparser.add_parser('cdf_compare',
                                    help='Compare 2 CDF files.')
    cdfcompare_parser.add_argument('cdf_compare', nargs='+',
                           help="Input CDF file paths")


    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)