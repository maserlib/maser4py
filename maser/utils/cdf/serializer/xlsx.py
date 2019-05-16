#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""Skt2xlsx module

Program to convert an input CDF skeleton table file
into an Excel format file (skt_editor).

"""


# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import logging
from copy import deepcopy

from openpyxl import Workbook

from maser.utils.cdf.serializer.globals import SHEETS, HEADER, GATTRS, ZVARS, VATTRS, NRV

__all__ = ["Skt2xlsx"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

# ________________ Class Definition __________
# (If required, define here classes)
class Skt2xlsx:
    """Class to convert a Skeleton object into a Excel 2007 format file."""

    def __init__(self, skeleton,
                 auto_pad=True):
        """__init__ method."""
        self.skeleton = deepcopy(skeleton)
        self.wb = None
        self.auto_pad = auto_pad


    def write_xlsx(self, output_path=None,
                  overwrite=False):
        """
        Write the Excel 2007 format file.

        :param output_path:
        :param overwrite: If true, overwrite existing output file
        :return:
        """

        if not output_path:
            xlsx = os.path.splitext(self.skeleton.file)[0] + ".xlsx"
        elif os.path.isdir(output_path):
            xlsx = os.path.join(output_path,
                               os.path.basename(
                                   os.path.splitext(self.skeleton.file)[0] + ".xlsx"
                               ))
        else:
            xlsx = output_path

        if not overwrite and os.path.isfile(xlsx):
            logger.warning("%s already exits!", xlsx)
            return xlsx

        logger.info("Writing %s...", xlsx)

        if not self.wb:
            logger.debug("Attempting to build Excel file body...")
            self._build_wb()

        self.wb.save(filename=xlsx)

        if os.path.isfile(xlsx):
            logger.info("{0} has been saved correctly".format(xlsx))
            return xlsx
        else:
            logger.error("{0} has not been saved correctly!".format(xlsx))
            return None

    def _build_wb(self):
        """
        Create Workbook from Skeleton object.

        :return:
        """
        wb = Workbook()

        # Create header sheet
        header_sheet = wb.create_sheet(title=HEADER)

        col_idx = 1
        for key, val in self.skeleton.header.items():
            if key not in SHEETS[HEADER]:
                continue
            # Make header of header in first row
            _ = header_sheet.cell(column=col_idx, row=1, value="{0}".format(key))
            # Add values in the second row
            _ = header_sheet.cell(column=col_idx, row=2, value="{0}".format(val))
            col_idx +=1

        # Create GLOBALattributes sheet
        gattrs_sheet = wb.create_sheet(title=GATTRS)

        # Make header of GLOBALatttributes in first row
        for i, key in enumerate(SHEETS[GATTRS]):
            _ = gattrs_sheet.cell(column=i+1, row=1, value="{0}".format(key))

        # Fill sheet with gattrs values
        row_idx = 2
        for key, entries in self.skeleton.gattrs.items():
            for i, entry in enumerate(entries):
                for j, col in enumerate(SHEETS[GATTRS]):
                    if entry[col] is None:
                        entry[col] = " "
                    _ = gattrs_sheet.cell(column=j+1, row=row_idx, value="{0}".format(
                    entry[col]))
                row_idx +=1

        # Create zVariables sheet
        zvars_sheet = wb.create_sheet(title=ZVARS)

        # Make header of zVariables in first row
        for i, key in enumerate(SHEETS[ZVARS]):
            _ = zvars_sheet.cell(column=i+1, row=1, value="{0}".format(key))

        # Fill sheet with zvars values
        row_idx = 2
        for zvar, entries in self.skeleton.zvars.items():
            for j, col in enumerate(SHEETS[ZVARS]):
                if entries[col] is None:
                    entry = " "
                elif isinstance(entries[col], list):
                    entry = " ".join(entries[col])
                else:
                    entry = entries[col]

                _ = zvars_sheet.cell(column=j+1, row=row_idx, value="{0}".format(
                    entry))
            row_idx +=1


        # Create VARIABLEattributes sheet
        vattrs_sheet = wb.create_sheet(title=VATTRS)

        # Make header of VARIABLEattributes in first row
        for i, key in enumerate(SHEETS[VATTRS]):
            _ = vattrs_sheet.cell(column=i+1, row=1, value="{0}".format(key))

        # Fill sheet with vattrs values
        row_idx = 2
        for zvar, vattrs in self.skeleton.vattrs.items():
            for vatt, entry in vattrs.items():
                # First column contains Variable name
                _ = vattrs_sheet.cell(column=1, row=row_idx, value="{0}".format(
                    zvar))
                for j, col in enumerate(SHEETS[VATTRS][1:]):
                    if entry[col] is None:
                        entry[col] = " "
                    _ = vattrs_sheet.cell(column=j+2, row=row_idx, value="{0}".format(
                        entry[col]))
                row_idx +=1

        # Create NRV sheet
        nrv_sheet = wb.create_sheet(title=NRV)

        # Make header of NRV in first row
        for i, key in enumerate(SHEETS[NRV]):
            _ = nrv_sheet.cell(column=i+1, row=1, value="{0}".format(key))

        row_idx = 2
        for zvar, fields in self.skeleton.zvars.items():
            if 'NRV' in fields:
                for i, entries in enumerate(fields["NRV"]):
                    for j, col in enumerate(SHEETS[NRV]):
                        if entries[col] is None:
                            entry[col] = " "
                        elif isinstance(entries[col], list):
                            entry = " ".join(entries[col])
                        else:
                            entry = entries[col]

                        _ = nrv_sheet.cell(column=j+1, row=row_idx, value="{0}".format(
                            entry))
                    row_idx +=1

        self.wb = wb

# ________________ Global Functions __________
def assign_pad(data_type):
    """VAR_PADVALUE auto assign.

    Automatically assigns VAR_PADVALUE
    depending to the input data_type
    """
    dtype = data_type.upper()

    if "EPOCH" in dtype:
        return "01-Jan-0000 00:00:00.000"
    elif "TT2000" in dtype:
        return "0000-01-01T00:00:00.000000000"
    elif ("INT" in dtype) or ("BYTE" in dtype):
        return "0"
    elif ("FLOAT" in dtype) or ("REAL" in dtype) or ("DOUBLE" in dtype):
        return "0.0"
    elif "CHAR" in dtype:
        return "\" \""
    else:
        return "None"

# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)