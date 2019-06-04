#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module containing the skeletoncdf subparser."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os

__all__ = ["add_skeletoncdf_subparser", "add_skeletontable_subparser"]

# ________________ HEADER _________________________


# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def add_skeletoncdf_subparser(subparser):
    """
    Subparser for cdf.serializer.skeletoncdf.

    :param subparser:
    :return:
    """
    sktcdf_parser = subparser.add_parser('skeletoncdf',
                                    help='Convert CDF skeleton table into binary CDF')
    sktcdf_parser.add_argument('skeletons', nargs='+',
                           help="Input CDF skeleton file(s)")
    sktcdf_parser.add_argument('-o', '--output_dir', nargs=1,
                        default=[os.getcwd()],
                        help='Path of the output directory')
    sktcdf_parser.add_argument('-e', '--executable', nargs=1,
                        default=[None],
                        help='Path of the skeletoncdf binary executable of the NASA CDF Toolkit.')
    sktcdf_parser.add_argument('-O', '--overwrite', action='store_true',
                        help='Overwrite existing output files')
    sktcdf_parser.add_argument('-F', '--force', action='store_true',
                        help='Force conversions even if an exception has raised')
    sktcdf_parser.add_argument('--no-auto-pad', action='store_true',
                        help='Deactivate automated assignment of the !VAR_PADVALUE')
    sktcdf_parser.add_argument('--no-cdf', action='store_true',
                        help='Do no generate output CDF "master" file')

def add_skeletontable_subparser(subparser):
    """
    Subparser for cdf.serializer.skeletontable.

    :param subparser:
    :return:
    """
    cdfskt_parser = subparser.add_parser('skeletontable',
                                          help='Convert CDF file into skeleton table')
    cdfskt_parser.add_argument('cdf', nargs='+',
                                help="Input CDF file(s)")
    cdfskt_parser.add_argument('-x', '--to-xlsx', action='store_true',
                                help='Input CDF also saved as Excel 2007 format file(s)')
    cdfskt_parser.add_argument('-o', '--output_dir', nargs=1,
                                default=[os.getcwd()],
                                help='Path of the output directory')
    cdfskt_parser.add_argument('-e', '--executable', nargs=1,
                                default=[None],
                                help='Path of the skeletontable binary executable of the NASA CDF Toolkit.')
    cdfskt_parser.add_argument('-O', '--overwrite', action='store_true',
                                help='Overwrite existing output files')
    cdfskt_parser.add_argument('-F', '--force', action='store_true',
                                help='Force conversions even if an exception has raised')

    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)
