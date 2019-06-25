#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module containing hfc subparser."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
from maser.services.helio.hfc.hfcviewer import DATE, OBSERVATORY, INSTRUMENT, TELESCOPE, WAVENAME, URL_WSDL

__all__ = ["add_hfcviewer_subparser"]

# ________________ HEADER _________________________




# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def add_hfcviewer_subparser(subparser):
    """cdf.validator script program."""

    hfcparser = subparser.add_parser('hfcviewer',
        help='HFC Viewer')
    hfcparser.add_argument('-d', '--date', nargs='?',
                        default=DATE,
                        help="Date of observation")
    hfcparser.add_argument('-o', '--observatory', nargs='?',
                        default=OBSERVATORY,
                        help="Name of the observatory")
    hfcparser.add_argument('-i', '--instrument', nargs='?',
                        default=INSTRUMENT,
                        help="Name of the instrument")
    hfcparser.add_argument('-t', '--telescope', nargs='?',
                        default=TELESCOPE,
                        help="Name of the telescope")
    hfcparser.add_argument('-w', '--wavename', nargs='?',
                        default=WAVENAME,
                        help="Name of the wavename")
    hfcparser.add_argument('-u', '--url_wsdl', nargs='?',
                        default=URL_WSDL,
                        help="Url of the wsdl file to load")
    hfcparser.add_argument('-x', '--xsize', nargs='?',
                        help="Window width on screen in pixels")
    hfcparser.add_argument('-y', '--ysize', nargs='?',
                        help="Window heigth on screen in pixels")
    hfcparser.add_argument('-Q', '--Quiet', action='store_true',
                        help="Quiet mode")
    hfcparser.add_argument('-D', '--Dev', action='store_true',
                        help="Run the development version of the hfcViewer")

    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)
