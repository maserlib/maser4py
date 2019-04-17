#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""cdf.serializer.txt module

Contains the class to manage the Skeleton table in text format.

"""


# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import logging
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from maser.settings import MASER_VERSION
from maser.utils.cdf.serializer.globals import VATTRS, JINJA_TEMPLATE_DIR

__all__ = ["Skt2txt"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__file__)


SKT_TEMPLATE = "skeleton.skt-tpl"

IN_FTIME = "%Y-%m-%dT%H:%M:%S"
NOW = datetime.now()
ROW_LENGTH_MAX = 79
DEF_INDENT = " " * 16

# ________________ Class Definition __________
# (If required, define here classes)
class Skt2txt:
    """Class to convert a Skeleton object into a CDF skeleton table."""

    def __init__(self, skeleton,
                 ignore_none=True,
                 auto_pad=True):
        """__init__ method."""
        self.skeleton = skeleton
        self.render = None
        self.ignore = ignore_none
        self.auto_pad = auto_pad

    def _build_render(self):
        """Build the CDF skeleton table content using the Skeleton object."""
        logger.debug("Building CDF skeleton table body... ")

        file = self.skeleton.file
        skt_name = os.path.splitext(os.path.basename(file))[0]

        # Setup jinja2 environment
        jenv = Environment(loader=FileSystemLoader(str(JINJA_TEMPLATE_DIR)))

        # Load MDOR template
        template = jenv.get_template(str(SKT_TEMPLATE))

        print(self.skeleton.zvars.keys())

        # Build the Skeleton template render
        self.render = template.render(
            gen_time=NOW.strftime(IN_FTIME),
            name=skt_name, version=MASER_VERSION,
            file=os.path.basename(file),
            header=self.skeleton.header,
            gattrs=self.reform_gattr(self.skeleton.gattrs),
            zvars=self.skeleton.zvars,
            vattrs=self.reform_vattr(self.skeleton.vattrs),
            vattrList=self.skeleton.cdf_items[VATTRS]
    )

    def reform_gattr(self, gattrs, length=48):
        """
        Re-format the global attributess to fit inside skeleton table
        (i.e., break too long line.)

        :param gattrs: list of g. attributes
        :return:
        """

        for gattr, entries in gattrs.items():
            for i, entry in enumerate(entries):
                value = ""
                counter = 0
                if str(entry["Value"]) == "None":
                    value = " "
                elif entry["Data Type"] != "CDF_CHAR":
                    continue
                else:
                    for char in entry["Value"]:
                        value += char
                        counter += 1
                        if counter > length:
                            value += '" - \n "'
                            counter = 0

                gattrs[gattr][i]["Value"] = value

        return gattrs


    def reform_vattr(self, vattrs, length=60):
        """
        Re-format the variable attributess to fit inside skeleton table
        (i.e., break too long line.)

        :param vattrs: list of v. attributes
        :return:
        """

        for zvar, entries in vattrs.items():
            for vatt, entry in entries.items():
                value = ""
                counter = 0
                if str(entry["Value"]) == "None":
                    value = " "
                elif entry["Data Type"] != "CDF_CHAR":
                    continue
                else:
                    for char in entry["Value"]:
                        value += char
                        counter += 1
                        if counter > length:
                            value += '" - \n "'
                            counter = 0

                vattrs[zvar][vatt]["Value"] = value

        return vattrs

    def write_txt(self, output_path=None,
                  overwrite=False):
        """Write the CDF skeleton table file."""

        if not output_path:
            txt = os.path.splitext(self.skeleton.file)[0] + ".skt"
        elif os.path.isdir(output_path):
            txt = os.path.join(output_path,
                               os.path.basename(
                                   os.path.splitext(self.skeleton.file)[0] + ".skt"
                               ))
        else:
            txt = os.path.splitext(output_path)[0] + ".skt"

        if not (overwrite) and (os.path.isfile(txt)):
            logger.warning("%s already exits!", txt)
            return txt

        logger.info("Writing %s...", txt)

        if not self.render:
            logger.warning("Attempting to build Skeleton table body...")
            self._build_render()

        with open(txt, "w") as filew:
            filew.write(self.render)

        if os.path.isfile(txt):
            logger.info("{0} has been saved correctly".format(txt))
            return txt
        else:
            logger.error("{0} has not been saved correctly!".format(txt))
            return None



# ________________ Global Functions __________



# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)