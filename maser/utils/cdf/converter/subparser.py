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
def add_skeletoncdf_subparser(subparser):
    """cdf.converter script program."""
    cdfconv_parser = subparser.add_parser('skeletoncdf',
                                    help='Convert CDF skeleton table into binary CDF')
    cdfconv_parser.add_argument('skeletons', nargs='+',
                           help="Input CDF skeleton file paths")
    cdfconv_parser.add_argument('-e', '--excel-format', action='store_true',
                        help='Input CDF skeleton provided as an Excel 2007 format file (.xlsx)')
    cdfconv_parser.add_argument('-o', '--output_dir', nargs=1,
                        default=[os.getcwd()],
                        help='Path of the output directory')
    cdfconv_parser.add_argument('-s', '--skeletoncdf', nargs=1,
                        default=[None],
                        help='Path of the skeletoncdf binary executable of the NASA CDF Toolkit.')
    cdfconv_parser.add_argument('-O', '--overwrite', action='store_true',
                        help='Overwrite existing output files')
    cdfconv_parser.add_argument('-I', '--ignore_none', action='store_true',
                        help='Ignore NoneType zVariables')
    cdfconv_parser.add_argument('-A', '--auto_pad', action='store_true',
                        help='Value of !VAR_PADVALUE ' +
                        'is automatically assigned')
    cdfconv_parser.add_argument('-F', '--force', action='store_true',
                        help='Force conversions even if an exception has raised')


    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)
