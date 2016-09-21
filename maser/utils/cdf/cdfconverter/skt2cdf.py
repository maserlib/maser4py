#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module to convert an CDF skeleton table (.skt) file
into a CDF master binary file (.cdf).
"""

# ________________ HEADER _________________________

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import os.path as osp
from datetime import datetime
import logging
import argparse

from ...toolbox import which, setup_logging, run_command

# ________________ HEADER _________________________

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

CURRENT_DATETIME = datetime.now()


# ________________ Class Definition __________
# (If required, define here classes)
class Skt2cdf:

    """ Class to convert a CDF skeleton table into a CDF master binary file"""

    def __init__(self, skt_file,
                 cdf_file=None,
                 output_dir=None,
                 overwrite=False,
                 verbose=True,
                 debug=False,
                 quiet=False):

        self.skt_file = skt_file
        self.overwrite = overwrite

        self.cdf_items = {}

        if cdf_file is None:
            cdf_file = osp.splitext(self.skt_file)[0] + ".cdf"

        if output_dir is None:
            output_dir = osp.basename(skt_file)
        else:
            cdf_file = osp.join(output_dir, os.path.basename(cdf_file))

        self.skt_file = skt_file
        self.cdf_file = cdf_file

    # Setup the logging
        setup_logging(
            filename=None, quiet=quiet,
            verbose=verbose,
            debug=debug)

    def make_master(self, exe=None):
        """make_master.

        Make a CDF Master binary file from a ASCII
        skeleton table using the skeletoncdf program.
        """
        cmd = []

        # If skeletoncdf program path is not provided
        # then search it on the $PATH
        if exe is None:
            if "CDF_BIN" in os.environ:
                exe = osp.join(os.environ["CDF_BIN"], "skeletoncdf")
            else:
                exe = which('skeletoncdf')

        if exe is None:
            logger.error("skeletoncdf PROGRAM IS NOT"
                " IN THE $PATH VARIABLE!")
            return None
        cmd.append(exe)

        if os.path.isfile(self.cdf_file) and self.overwrite:
            logger.warning("%s existing file will be overwritten!",
                           self.cdf_file)
            cmd.append("-delete")

        cmd.append(self.skt_file)
        cmd.extend(["-cdf", self.cdf_file])
        res = run_command(cmd)
        output, errors = res.communicate()
        if res.wait() == 0:
            logger.debug(output)
            if os.path.isfile(self.cdf_file):
                logger.info(self.cdf_file + " has been saved correctly!")
                return self.cdf_file
            else:
                logger.error(self.cdf_file + " has not been saved correctly!")
                return None
        else:
            logger.error("ERROR RUNNING COMMAND: ")
            logger.error(" ".join(cmd))
            logger.error("STDOUT - %s", str(output))
            logger.error("STDERR - %s", str(errors))
            return None


# ________________ Global Functions __________
def main():

    """
    skt2cdf main method
    """

    parser = argparse.ArgumentParser(
        description='Convert a CDF skeleton table file' +
        ' into a CDF master binary file',
        add_help=True)
    parser.add_argument('skeleton', nargs=1,
                        default=None,
                        help='Skeleton table to convert')
    parser.add_argument('-c', '--cdf', nargs='?',
                        default=None,
                        help='Output CDF master file (.cdf)')
    parser.add_argument('-s', '--skeletoncdf', nargs='?',
                        default=None,
                        help='Path of the skeletoncdf binary executable')
    parser.add_argument('-o', '--output_dir', nargs='?',
                        default=None,
                        help='Path of the output directory')
    parser.add_argument('-O', '--Overwrite', action='store_true',
                        help='Overwrite existing output files')
    parser.add_argument('-V', '--Verbose', action='store_true',
                        help='Verbose mode')
    parser.add_argument('-D', '--Debug', action='store_true',
                        help='Debug mode')
    parser.add_argument('-Q', '--Quiet', action='store_true',
                        help='Quiet mode')
    args = parser.parse_args()

    Skt2cdf(args.skeleton[0], cdf_file=args.cdf,
            output_dir=args.output_dir,
            overwrite=args.Overwrite, verbose=args.Verbose,
            debug=args.Debug,
            quiet=args.Quiet).make_master(exe=args.skeletoncdf)


# _________________ Main ____________________________
if __name__ == "__main__":
    main()
