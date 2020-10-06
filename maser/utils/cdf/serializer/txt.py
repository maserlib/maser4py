#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""cdf.serializer.txt module

Contains the class to manage the Skeleton table in text format.

"""


# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import re
import logging
from datetime import datetime
from copy import deepcopy

from jinja2 import Environment, FileSystemLoader

from maser.settings import MASER_VERSION
from maser.utils.cdf.serializer.exceptions import InvalidFile
from maser.utils.cdf.serializer.globals import JINJA_TEMPLATE_DIR
from maser.utils.cdf.serializer.globals import SHEETS, HEADER, GATTRS, ZVARS, \
    RVARS, VATTRS, NRV, END
from maser.utils.cdf.serializer.globals import NEW_HEADER, NEW_ZVAR, NEW_VATTRS, NO_NRV, NEW_NRV


__all__ = ["Skt2txt", "Txt2skt"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)


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
        self.skeleton = deepcopy(skeleton)
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

        # Load skeleton table template
        template = jenv.get_template(str(SKT_TEMPLATE))

        # Build the Skeleton template render
        self.render = template.render(
            gen_time=NOW.strftime(IN_FTIME),
            name=skt_name,
            version=MASER_VERSION,
            file=os.path.basename(file),
            header=self.skeleton.header,
            gattrs=self.reform_gattr(self.skeleton.gattrs),
            zvars=self.skeleton.zvars,
            vattrs=self.reform_vattr(self.skeleton.vattrs),
            vattrList=self.skeleton.vattrList
        )

    def reform_gattr(self, gattrs, length=48):
        """
        Re-format the global attributess to fit inside skeleton table
        (i.e., break too long line.)

        :param gattrs: list of g. attributes
        :return:
        """

        new_gattr = dict()
        for gattr, entries in gattrs.items():
            for i, entry in enumerate(entries):
                value = ""
                counter = 0
                if str(entry["Value"]) == "None":
                    value = " "
                elif entry["Data Type"] != "CDF_CHAR":
                    continue
                else:
                    for char in str(entry["Value"]):
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
                                   os.path.splitext(self.skeleton.file)[
                                       0] + ".skt"
                               ))
        else:
            txt = os.path.splitext(output_path)[0] + ".skt"

        if not (overwrite) and (os.path.isfile(txt)):
            logger.warning("%s already exits!", txt)
            return txt

        logger.info("Writing %s...", txt)

        if not self.render:
            logger.debug("Attempting to build Skeleton table body...")
            self._build_render()

        with open(txt, "w") as filew:
            filew.write(self.render)

        if os.path.isfile(txt):
            logger.info("{0} has been saved correctly".format(txt))
            return txt
        else:
            logger.error("{0} has not been saved correctly!".format(txt))
            return None


class Txt2skt:
    """Class to convert a CDF skeleton table file into a Skeleton object."""

    def __init__(self, skeleton):

        self.file = None
        self.skeleton = skeleton
        self.section = None
        self.row = ""

    def parse_txt(self, txt_file):
        """
        Parse input CDF skeleton table file

        :param txt_file: Path to CDF skeleton table file
        :return:
        """
        self.file = txt_file
        if not os.path.isfile(txt_file):
            logger.error("{0} NOT FOUND, ABORTING!".format(txt_file))
            raise FileNotFoundError
        else:
            self.file = txt_file

        zvar = None
        new_header = False
        new_zvar = False
        new_vattrs = False
        new_nrv = False
        gattname = None
        for row in self.txt_iterator():
            cols = [col for col in re.split('\[|\]| |\'|\n', row) if col]
            ncols = len(cols)
            # Get "compressed" row, i.e., without any empty space
            row_c = "".join(cols)

            logger.debug(row_c)

            # Enter into the header section
            if self.section == HEADER:

                if row_c == NEW_HEADER:
                    new_header = True
                    continue
                elif row_c.startswith("!-"):
                    continue
                elif new_header:
                    self.skeleton.header["nzvar"] = cols[0].split("/")[1]
                    self.skeleton.header["ngattr"] = cols[1]
                    self.skeleton.header["nvattr"] = cols[2]
                    new_header = False
                    continue

                for field in SHEETS[HEADER]:
                    if field in row:
                        self.skeleton.header[field] = row.strip().split(":")[
                            1].strip()
                        break
                    elif row.startswith("!") or ncols == 0:
                        continue

            # Enter into the global attribute definition section
            elif self.section == GATTRS:
                # Skip comment/empty line
                if row_c.startswith("!") or ncols == 0:
                    continue
                else:
                    # If it is a global attribute definition row...
                    self.row += " " + row

                if row_c.endswith('}') or row_c.endswith('}.'):
                    # If gattname already defined, it means that it is a new entry
                    # Then append the name of g. attribute for the field
                    # extraction
                    if gattname:
                        self.row = '"{0}" '.format(gattname) + self.row
                    # Extract field for the current g.attribute entry
                    gatt_desc = self._extract_attr()
                    # Store the g.attribute fields into self.skeleton.gattrs
                    if gatt_desc["Attribute Name"] in self.skeleton.gattrs:
                        self.skeleton.gattrs[
                            gatt_desc["Attribute Name"]].append(gatt_desc)
                    else:
                        self.skeleton.gattrs[
                            gatt_desc["Attribute Name"]] = [gatt_desc]

                    # Define gatt_desc["Attribute Name"] as the current
                    # gattname
                    gattname = gatt_desc["Attribute Name"]

                    self.row = ""

                # If it is the end of the global attribute definition,
                # Reset the gattname
                if row_c.endswith('.'):
                    gattname = None
                    self.row = ""

            # Enter into the variable attribute list section
            elif self.section == VATTRS:
                # Skip comment/empty line
                if row.startswith("!") or row == "":
                    continue
                else:
                    self.skeleton.vattrList.append(row.split('"')[1])

            # Enter into the zVariable definition section
            elif self.section == ZVARS:

                # Retrieve value of the VAR_COMPRESSION parameter
                if "!VAR_COMPRESSION:" in row_c:
                    value = row.strip().split(":")
                    nval = len(value)
                    if nval == 2:
                        value = value[1]
                    elif nval > 2:
                        value = ":".join(value[1:])
                    else:
                        logger.error(
                            "VAR_COMPRESSION seems to be badly formatted!")
                        raise InvalidFile

                    self.skeleton.zvars[zvar]["VAR_COMPRESSION"] = value
                # Retrieve value of the VAR_PADVALUE parameter
                elif "!VAR_PADVALUE:" in row_c:
                    value = row.strip().split(":")
                    nval = len(value)
                    if nval == 2:
                        value = value[1]
                    elif nval > 2:
                        value = ":".join(value[1:])
                    else:
                        logger.error(
                            "VAR_PADVALUE seems to be badly formatted!")
                        raise InvalidFile
                    self.skeleton.zvars[zvar]["VAR_PADVALUE"] = value
                # Retrieve value of the VAR_SPARSERECORDS parameter
                elif "!VAR_SPARSERECORDS:" in row_c:
                    value = row.strip().split(":")
                    nval = len(value)
                    if nval == 2:
                        value = value[1]
                    elif nval > 2:
                        value = ":".join(value[1:])
                    else:
                        logger.error(
                            "VAR_SPARSERECORDS seems to be badly formatted!")
                        raise InvalidFile
                    self.skeleton.zvars[zvar]["VAR_SPARSERECORDS"] = value
                elif row_c == NEW_ZVAR:
                    # New zvariable definition sub-section has been found
                    new_nrv = False
                    new_zvar = True
                    zvar = None
                    self.row = ""
                elif (new_zvar and row_c.startswith('"') and
                      not (row_c.endswith('F') or row_c.endswith('T'))):
                    # variable definition is on several lines
                    # store these lines in self.row
                    self.row += " " + row
                elif new_zvar and (row_c.endswith('F') or row_c.endswith('T')):
                    if not self.row:
                        self.row = row
                    else:
                        self.row += " " + row
                    # Extract line containing zvariable structure (name, data type, num elem, dims, sizes
                    # rec. variance and dim variances)
                    zvar_desc = self._extract_zvar()
                    zvar = zvar_desc["Variable Name"]

                    # Initialize the zvars dictionary in Skeleton object for
                    # the given zvar
                    self.skeleton.zvars[zvar] = dict()
                    self.skeleton.zvars[zvar][NRV] = []

                    # fill the zvars dictionary in Skeleton object
                    for key in SHEETS[ZVARS]:
                        if key in zvar_desc:
                            self.skeleton.zvars[zvar][key] = zvar_desc[key]
                        else:
                            self.skeleton.zvars[zvar][key] = None
                elif new_zvar and row_c == NEW_VATTRS:
                    # New variable attribute definitions found for the current
                    # zvariable
                    new_zvar = False
                    new_vattrs = True
                    # Initialize the vattrs dictionary in Skeleton object for
                    # the given zvariable
                    self.skeleton.vattrs[zvar] = dict()
                    self.row = ""
                elif new_vattrs and row_c.startswith('"') and row_c.endswith('"-'):
                    # variable attribute definition is on several lines
                    # store these lines in self.row
                    self.row += " " + row
                elif new_vattrs and row_c.startswith('"') and row_c.endswith('"'):
                    # variable attribute definition is on several lines
                    # store these lines in self.row
                    self.row += " " + row
                elif ((new_vattrs and row_c.endswith("}")) or
                      (new_vattrs and row_c.endswith("}."))):
                    # End of the variable attribute definition, extract fields
                    # inside the row
                    if not self.row:
                        self.row = row
                    else:
                        self.row += " " + row
                    vatt_desc = self._extract_attr()

                    # And store them into the vattrs dictionary in Skeleton
                    # object
                    if vatt_desc["Attribute Name"] in self.skeleton.vattrs[zvar]:
                        logger.error("{0} is defined twice for {1} variable!".format(
                            vatt_desc["Attribute Name"],
                            zvar
                        ))
                    else:
                        self.skeleton.vattrs[zvar][
                            vatt_desc["Attribute Name"]] = vatt_desc
                    self.row = ""
                elif row_c == NO_NRV:
                    new_vattrs = False
                elif row_c == NEW_NRV:
                    new_vattrs = False
                    new_nrv = True
                elif new_nrv and "=" in row_c:
                    fields = self._extract_nrv(zvar, row)
                    self.skeleton.zvars[zvar][NRV].append(fields)
                # Skip comment/empty line
                elif row_c.startswith("!") or ncols == 0:
                    continue

        self.skeleton.file = self.file
        self.skeleton.xlsx = False
        return self.skeleton

    def txt_iterator(self):
        """
        Method to iter over rows of an input CDF skeleton table file.
        (rVariable parsing not supported)

        :param txt_file:
        :return: row
        """

        with open(self.file, 'rt') as txt:
            for row in txt.readlines():
                logger.debug(row)

                # Read header
                if row.startswith("#" + HEADER):
                    self.section = HEADER

                # Read GLOBALattributes
                elif row.startswith("#" + GATTRS):
                    self.section = GATTRS

                # Read VARIABLEattributes
                elif row.startswith("#" + VATTRS):
                    self.section = VATTRS

                # Skip rVariables (not supported)
                elif row.startswith("#" + RVARS):
                    logger.debug("rVariables parsing not supported")
                    continue
                # Read zVariables
                elif row.startswith("#" + ZVARS):
                    self.section = ZVARS

                # End of the file
                elif row.startswith("#" + END):
                    # check that everything is correctly defined
                    if not self.skeleton.header:
                        logger.warning("{0} is missing".format(HEADER))
                    else:
                        logger.debug(HEADER + ":" + str(self.skeleton.header))
                    if not self.skeleton.gattrs:
                        logger.warning("{0} is missing".format(GATTRS))
                    else:
                        logger.debug(GATTRS + ":" + str(self.skeleton.gattrs))
                    if not self.skeleton.vattrs:
                        logger.warning("{0} is missing".format(VATTRS))
                    else:
                        logger.debug(VATTRS + ":" + str(self.skeleton.vattrs))
                    if not self.skeleton.zvars:
                        logger.warning("{0} is missing".format(ZVARS))
                    else:
                        logger.debug(ZVARS + ":" + str(self.skeleton.zvars))

                else:
                    yield row.strip()

    def _extract_attr(self):
        """
        Extract attribute from row.


        :return:
        """

        row = self.row
        # if a dot at the end of the row, then remove it
        if row.endswith("."):
            row = row[:-1]

        items = row.split()

        # Remove possible quotes at the start/end
        if items[0].startswith('"') and items[0].endswith('"'):
            attname = items[0][1:-1]
        else:
            attname = items[0]

        # If { is the first character, then it is a variable attribute
        if items[2].startswith("{"):
            entry = None
            i = 1
        # else it is a global attribute
        else:
            entry = items[1].split(":")[0]
            i = 2

        dtype = items[i]

        if dtype == "CDF_CHAR" or dtype == "CDF_UCHAR":
            att_pattern = '\{ "([\S ]*)" \}'
        else:
            att_pattern = '\{ ([\S ]*) \}'

        # Join value items
        value = " ".join(items[i + 1:])

        # Remove line breaks
        value = "".join(value.split('" - "'))
        value = "".join(value.split('"- "'))
        value = "".join(value.split('" -"'))
        value = "".join(value.split('"-"'))

        # Extract attribute value from {}
        # (Use regex to make sure that it is a well formatted value)
        value = re.findall(att_pattern, value)

        if not value:
            logger.error("No value for {0}".format(attname))
            raise InvalidFile
        else:
            return dict(zip(SHEETS[GATTRS], [attname, entry, dtype, value[0]]))

    def _extract_nrv(self, zvar, row):
        """
        Extract a nrv entry

        :param row:
        :return:
        """
        items = row.strip().split("=")
        if len(items) != 2:
            logger.error("Wrong NRV for {0}".format(zvar))
            raise InvalidFile

        index = items[0].strip()[1:-1]
        value = items[1].strip()
        if value.startswith("{"):
            value = re.findall('\{ "([\S ]*)" \}', value)

        if isinstance(value, list):
            value = "".join(value).strip()

        return dict(zip(SHEETS[NRV], [zvar, index.strip(), value]))

    def _extract_zvar(self):
        """
        Extract a zvar definition

        :param row:
        :return:
        """
        row = self.row
        items = row.split()
        name = items[0][1:-1]
        dtype = items[1]
        elem = items[2]
        dims = items[3]
        if dims == "0":
            sizes = None
            recvar = items[4]
            dimvar = None
        else:
            i = 4
            sizes = []
            for j in range(i, i + int(dims), 1):
                sizes.append(items[j])
            i = j + 1
            recvar = items[i]
            i += 1
            dimvar = []
            for j in range(i, i + int(dims)):
                dimvar.append(items[j])

        x = [name, dtype, elem, dims, sizes, recvar, dimvar]

        return dict(zip(SHEETS[ZVARS][:8], x))
# ________________ Global Functions __________


# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)
