#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module template."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os

# ________________ HEADER _________________________


# ________________ Global Variables _____________
# (define here the global variables)
LS_FILENAME = "CDFLeapSeconds.txt"

CURDIR = os.path.dirname(os.path.abspath(__file__))
LS_FILE_DEF_DIR = os.path.join(CURDIR,
                               "..", "..",
                                     "support", "data")
if not os.path.isdir(LS_FILE_DEF_DIR):
    os.makedirs(LS_FILE_DEF_DIR)
LS_FILE_DEF_PATH = os.path.join(LS_FILE_DEF_DIR, LS_FILENAME)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def add_leapsec_subparser(subparser):
    """cdf.serializer script program."""
    leapsec_parser = subparser.add_parser('leapsec',
                                    help='Leapsecond handling tool')
    leapsec_parser.add_argument("-f", "--filepath",
                        nargs=1, default=[LS_FILE_DEF_PATH],
                        help="CDFLeapSeconds.txt filepath.\n "
                        "Default is ${0}".format(LS_FILE_DEF_PATH))
    leapsec_parser.add_argument("-d", "--date", nargs=1,
                        default=[None],
                        help="Return the leap seconds for "
                        "a given date and time."
                        "(Expected format is \"YYYY-MM-DDThh:mm:ss\")")
    leapsec_parser.add_argument("-D", "--DOWNLOAD-FILE", action='store_true',
                        help="Download the CDFLeapSeconds.txt file"
                        "from the NASA CDF Web site. "
                        "The file will be saved in the path"
                        " defined in the --filepath argument.")
    leapsec_parser.add_argument("-S", "--SHOW-TABLE", action='store_true',
                        help="Show the leap sec. table")
    leapsec_parser.add_argument("-O", "--OVERWRITE", action='store_true',
                        help="Overwrite existing file")


    # _________________ Main ____________________________
# if __name__ == "__main__":
#     print(__file__)
