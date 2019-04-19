#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""parse_skt module.

Program to parse an input CDF skeleton table file.

"""


# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from maser.utils.cdf.serializer.txt import Skt2txt, Txt2skt
from maser.utils.cdf.serializer.xlsx import Skt2xlsx, Xlsx2skt
from maser.utils.cdf.serializer.globals import SHEETS, HEADER, GATTRS, ZVARS, VATTRS, NRV

__all__ = ["Skeleton"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__file__)



# ________________ Class Definition __________
# (If required, define here classes)
class Skeleton():

    def __init__(self):
        """
        Init method of the Skeleton class.

        :param skeleton_file:
        """

        self.file = None
        self.cdf_items = dict()
        self.header = dict()
        self.gattrs = dict()
        self.vattrs = dict()
        self.vattrList = []
        self.zvars = dict()
        self.xlsx = False

    @staticmethod
    def from_txt(txt_file):
        """
        Create a Skeleton instance from the input text file.

        :param txt_file:
        :return: an instance of Skeleton
        """

        skeleton = Skeleton()
        return Txt2skt(skeleton).parse_txt(txt_file)

    @staticmethod
    def from_xlsx(xlsx_file, auto_pad=True):
        """
        Create a Skeleton instance from the input Excel file.

        :param xlsx_file: input Excel file to convert to Skeleton object
        :param auto_pad: If True assigns automatic value to VAR_PADVALUE
        :return: an instance of Skeleton
        """
        skeleton = Skeleton()
        return Xlsx2skt(skeleton).parse_xlsx(xlsx_file, auto_pad=auto_pad)

    def to_txt(self, output_path=None,
               overwrite=False):
        """
        Convert a Skeleton object into an output Skeleton table file in ASCII format.

        :param output_path: Path of the output Skeleton table file
        :param overwrite: If True, the overwrite existing output file
        :return: Path of the output file
        """

        return Skt2txt(self).write_txt(output_path=output_path,
                                              overwrite=overwrite)

    def to_xlsx(self, output_path=None,
               overwrite=False):
        """
        Convert a Skeleton object into an output Excel 2007 format file.

        :param output_path: Path of the output Excel file
        :param overwrite: If True, the overwrite existing output file
        :return: Path of the output file
        """

        return Skt2xlsx(self).write_xlsx(output_path=output_path,
                                              overwrite=overwrite)


    def is_valid_gatt(self, entries):
        """
        Check that the input is a valid gattrs entry.

        :param entries:
        :return: True if it is valid
        """
        for entry in entries:
            for field in SHEETS[GATTRS]:
                if field not in entry:
                    logger.error("{0} field is missing, aborting!")
                    return False

        return True

    def is_valid_zvar(self, entry):
        """
        Check that the input is a valid zvars entry.

        :param entry:
        :return: True if it is valid
        """
        for field in SHEETS[ZVARS]:
            if field not in entry:
                logger.error("{0} field is missing, aborting!")
                return False

        return True

    def is_valid_vattrs(self, entry):
        """
        Check that the input is a valid vattrs.

        :param entry:
        :return: True if it is valid
        """

        for key, val in entry.items():
            for field in SHEETS[VATTRS]:
                if field not in val:
                    logger.error("{0} field is missing, aborting!")
                    return False

        return True
# ________________ Global Functions __________



# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)