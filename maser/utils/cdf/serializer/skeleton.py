#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""parse_skt module.

Program to parse an input CDF skeleton table file.

"""


# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import logging

from maser.utils.cdf.serializer.exceptions import InvalidEntry
from maser.utils.cdf.serializer.txt import Skt2txt, Txt2skt
from maser.utils.cdf.serializer.xlsx import Skt2xlsx, Xlsx2skt
from maser.utils.cdf.serializer.globals import SHEETS, HEADER, \
    GATTRS, ZVARS, VATTRS

__all__ = ["Skeleton"]

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)



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


    def is_valid_header(self, header, ignore=[]):
        """
        Check that the input is a valid cdf header.

        :param header: header dictionary
        :param ignore: List of field(s) to ignore
        :return: True if the header is valid
        """

        for entry in header:
            for field in SHEETS[HEADER]:
                if field in ignore:
                    continue
                if field not in entry:
                    logger.warning("{0} field is missing!".format(field))
                    return False

        return True

    def is_valid_gatt(self, entries, ignore=[]):
        """
        Check that the input gattr entries are valid.

        :param entries: Entries to check
        :param ignore: list of field(s) to ignore
        :return: True if it is valid
        """
        for entry in entries:
            for field in SHEETS[GATTRS]:
                if field in ignore:
                    continue
                if field not in entry:
                    logger.warning("{0} field is missing!".format(field))
                    return False

        return True

    def is_valid_zvar(self, entry, ignore=[]):
        """
        Check that the input is a valid zvars entry.

        :param entry: entry to check
        :param ignore: list of field(s) to ignore
        :return: True if it is valid
        """
        for field in SHEETS[ZVARS]:
            if field in ignore:
                continue
            if field not in entry:
                logger.warning("{0} field is missing!".format(field))
                return False

        return True

    def is_valid_vattrs(self, entry, ignore=[]):
        """
        Check that the input is a valid vattrs.

        :param entry: entry to check
        :param ignore: list of field(s) to ignore
        :return: True if it is valid
        """

        for field in SHEETS[VATTRS]:
            if field in ignore:
                continue
            if field not in entry :
                logger.warning("{0} field is missing!".format(field))
                return False

        return True


    def set_header(self, entry):
        """
        Set header field(s)

        :param entry: dictionary containing header field(s) to udpate
        :return:
        """
        for key, val in entry.items():
            if key not in SHEETS[HEADER]:
                logger.warning("Unknown field: {0}!".format(key))
                continue
            self.header[key] = val

        return True

    def add_gattr(self, attname, entries,
                  append=False):
        """
        Add a global attribute to the Skeleton object.


        :param attname: name of the g. attribute to add
        :param entries: List containing the entries for the g.attribute
        :param append: If True, then append input entries to the existing one(s)
        """

        logger.info("Adding entries for g.attribute {0}".format(attname))
        if attname in self.gattrs and append:
            # Check that all the expected fields are in the input entries
            if not self.is_valid_gatt(entries,
                                      ignore=["Entry Number",
                                              "Attribute Name",
                                              "Data Type"]):
                raise InvalidEntry


            # Get number of entries
            nentry = len(self.gattrs[attname])
            for i, entry in enumerate(entries):
                entry["Attribute Name"] = attname
                entry["Data Type"] = self.gattrs[attname][0]["Data Type"]
                entry["Entry Number"] = str(nentry + 1)
                self.gattrs[attname].append(entry)

            return True

        elif attname in self.gattrs:
            logger.warning("{0} already exists!".format(attname))
            return False
        else:
            # Check that all the expected fields are in the input entries
            if not self.is_valid_gatt(entries):
                raise InvalidEntry

            self.gattrs[attname] = entries
            self.header["ngattr"] = str(int(self.header["ngattr"]) + 1)
            return True

    def set_gattr(self, attname, new_entry, add=False):
        """
        Update an entry for a given g.attribute in the Skeleton object.

        :param attname: name of the g.attribute to update
        :param new_entry: new entry values provided as a dictionary
        :param add: If g.attribute does not exist, then add it with the input entries
        :return:
        """
        logger.info("Updating g.attribute {0}".format(attname))
        # Check if the attribute already exists
        if attname not in self.gattrs:
            logger.warning(
                "{0} g.attribute does not exist!".format(
                    attname))
            if not add:
                return False
            else:
                return self.add_gattr(attname, [new_entry])

        # Check if the Entry Number is provided in the new_entry dictionary
        if "Entry Number" not in new_entry:
            logger.error("No Entry Number provided!")
            raise InvalidEntry

        # Loop over self.gattrs[attname] to look for the entry number to update
        has_entry = False
        for i, entry in enumerate(self.gattrs[attname]):
            # If found, then retrieve the new entry values and save them into self.gattrs[attname]
            if self.gattrs[attname][i]["Entry Number"] == new_entry["Entry Number"]:
                for key, val in new_entry.items():
                    if key not in SHEETS[GATTRS]:
                        logger.warning("Unknown field: {0}!".format(key))
                        continue
                    self.gattrs[attname][i][key] = new_entry[key]
                    has_entry = True

        if has_entry == False:
            logger.warning("Entry Number {0} not found!".format(new_entry["Entry Number"]))

        return has_entry

    def rename_gattr(self, old_attname, new_attname):
        """
        Rename a global attr. from the Skeleton object.

        :param old_attname:
        :param new_attname:
        :return:
        """
        logger.info("Renaming g.attribute {0} into {1}".format(old_attname, new_attname))
        # Check if the zVariable already exists
        if old_attname not in self.gattrs:
            logger.error(
                           "{0} g.attribute does not exist!".format(
                               old_attname))
            return False
        else:
            self.gattrs[new_attname] = self.gattrs[old_attname]
            for i, entry in enumerate(self.gattrs[new_attname]):
                self.gattrs[new_attname][i]["Attribute Name"] = new_attname
            del self.gattrs[old_attname]
            return True

    def rm_gattr(self, attname):
        """
        Remove a global attr. from the Skeleton object.

        :param skeleton:
        :param attname:
        :return:
        """
        logger.info("Removing g.attribute {0}".format(attname))
        if attname in self.gattrs:
            del self.gattrs[attname]
            self.header["ngattr"] -= 1


    def add_vattr(self, attname, entry, varname=None, add=False):
        """
        Add entries for a variable attribute into the Skeleton object.

        :param attname: name of the v. attribute to add
        :param entry: List containing the entry for the v.attribute
        :param varname: If provided, contains a list of zvariable for which the v.attribute must be added. If not provided v.attribute is added for all the variables.
        :add: If True, add vattr entry to zvariable(s)
        :return:
        """
        if attname not in self.vattrList:
            self.vattrList.append(attname)
            self.header["nvattr"] +=1

        # Add Attribute Name value if not provided
        if 'Attribute Name' not in entry:
            entry['Attribute Name'] = attname

        # Check that all the expected fields are in the input entries
        if not self.is_valid_vattrs(entry,
                                    ignore=["Variable Name"]):
            raise InvalidEntry

        # If varname not provided, then add variable attribute for all variables
        if not varname:
            varname = self.vattrs.keys()
        else:
            for var in varname:
                if var not in self.vattrs:
                    if not add:
                        logger.error("{0} not found in vattrs!".format(var))
                        raise InvalidEntry
                    else:
                        self.vattrs[var] = dict()

        for zvar in varname:
            logger.info("Adding v.attribute {0} for {1}".format(attname, zvar))
            entry['Variable Name'] = zvar
            self.vattrs[zvar][attname] = entry

        return True

    def set_vattr(self, attname, entry, varname=None):
        """
        Set a given v.attribute

        :param attname: name of the v. attribute to set
        :param entry: List containing the entry for the v.attribute
        :param varname: If provided, contains a list of zvariable for which the v.attribute must be set. If not provided v.attribute is set for all the variables.
        :return:
        """
        logger.info("Updating v.attribute {0}".format(attname))
        # Check if the attribute already exists
        if attname not in self.vattrList:
            logger.error(
                "{0} v.attribute does not exist!".format(
                    attname))
            return False
        else:

            # Variable name can be also provided in the entry
            if 'Variable Name' in entry:
                varname = [entry['Variable Name']]

            if not varname:
                varname = self.vattrs.keys()
            else:
                for var in varname:
                    if var not in self.vattrs:
                        logger.error("{0} not found!".format(var))
                        raise InvalidEntry

            for var in varname:
                for key, val in entry.items():
                    if key not in SHEETS[VATTRS]:
                        logger.warning("Unknown field: {0}!".format(key))
                        continue
                    self.vattrs[var][attname][key] = val


    def rename_vattr(self, old_attname, new_attname, varname=None):
        """
        Rename a variable attr. from the Skeleton object.

        :param old_attname: current name of the v.attribute
        :param new_attname: new new of the v.attribute
        :param varname: If provided, rename only for the given zVariables in the varname list. Else rename all.
        :return:
        """
        logger.info("Renaming v.attribute {0} into {1}".format(old_attname, new_attname))
        # Check if the zVariable already exists
        if old_attname not in self.vattrList:
            logger.error(
                           "{0} v.attribute does not exist!".format(
                               old_attname))
            return False
        else:
            self.vattrList[new_attname] = self.vattrList[old_attname]
            del self.vattrList[old_attname]

            if old_attname in self.vattrList:
                self.vattrList[new_attname] = self.vattrList[old_attname]
                del self.vattrList[old_attname]

        if not varname:
            varname = self.vattrs.keys()
        else:
            for var in varname:
                if var not in self.vattrs:
                    logger.error("{0} not found!".format(var))
                    raise InvalidEntry

        # Check for each zvar too
        for var in varname:
            if old_attname in self.vattrs[var]:
                self.vattrs[var][new_attname] = self.vattrs[var][old_attname]
                del self.vattrs[var][old_attname]

        return True

    def rm_vattr(self, attname, varname=None):
        """
        Remove a variable attr. from the Skeleton object.

        :param attname: Name of the v.attribute to remove
        :param varname: if provided, only remove the v.attribute for the given list of zVariable in the varname input. Else remove all.
        :return:
        """
        logger.info("Removing v.attribute {0}".format(attname))
        if attname in self.vattrList:
            del self.vattrList[attname]
            self.header["nvattr"] -= 1

        if not varname:
            varname = self.vattrs.keys()
        else:
            for var in varname:
                if var not in self.vattrs:
                    logger.error("{0} not found!".format(var))
                    raise InvalidEntry

        # also check for each zvar
        for var in varname:
            if attname in self.vattrs[var]:
                del self.vattrs[var][attname]


    def add_zvar(self, varname, entry, vattrs=None):
        """
        Add a zVariable into the Skeleton object.

        :param varname: name of the zVariable to add
        :param entry: dictionary with fields to add [variable name, data type, number elements,
                    dims, sizes, record variance, Dimension variances]. If dims=0, sizes and record variance must be None
        :param vattrs: dictionnary containing variable attribute(s) to load for this zvariable. V.attributes can be also provided in the entry using the "Variable attributes" dictionary keyword.
        :return:
        """
        logger.info("Adding zvariable {0}".format(varname))
        # Check if the zVariable already exists
        if varname in self.zvars:
            logger.warning(
                           "{0} variable already exists!".format(
                                                        varname))
            return False
        else:
            # Check content
            if not self.is_valid_zvar(entry):
                raise InvalidEntry
            # Add the zvariable
            self.zvars[varname] = entry
            self.header["nzvar"] += 1

            # if entry contains the "Variable Attributes" keyword, then extract it to get vattrs
            if "Variable Attribute" in entry:
                vattrs = entry["Variable Attributes"]

            # if Variable attributes are provided for this zVariable, then add them.
            if vattrs:
                for vattname, vattentry in vattrs.items():
                    self.add_vattr(vattname, vattentry, varname=[varname], add=True)

        return True

    def set_zvar(self, varname, entry, vattrs=None):
        """
        Update zvariable entry into the Skeleton object.

        :param varname:
        :param entry:
        :param vattrs:
        :return:
        """
        logger.info("Updating zvariable {0}".format(varname))
        # Check if the zVariable already exists
        if varname not in self.zvars:
            logger.error(
                           "{0} variable does not exist!".format(
                                                        varname))
            return False
        else:
            # update the zvariable

            for field in SHEETS[ZVARS]:
                if field in entry:
                    self.zvars[varname][field] = entry[field]
                else:
                    continue

            # if entry contains the "Variable Attributes" keyword, then extract it to get vattrs
            if "Variable Attribute" in entry:
                vattrs = entry["Variable Attributes"]

            if vattrs:
                if varname not in self.vattrs:
                    logger.warning(
                        "{0} variable has no variable attribute, add input!".format(
                            varname))
                    self.vattrs[varname] = dict()

                for key, val in vattrs.items():
                    if key not in SHEETS[VATTRS]:
                        logger.warning("Unknown field: {0}!".format(key))
                        continue
                    self.vattrs[varname][key] = val

        return True

    def rename_zvar(self, old_varname, new_varname):
        """
        Rename a zVariable of the Skeleton object.

        :param old_varname:
        :param new_varname:
        :return:
        """
        logger.info("Renaming zvariable {0} into {1}".format(old_varname, new_varname))
        # Check if the zVariable already exists
        if old_varname not in self.zvars:
            logger.error(
                           "{0} variable does not exist!".format(
                               old_varname))
            return False
        else:
            self.zvars[new_varname] = self.zvars[old_varname]
            self.zvars[new_varname]['Variable Name'] = new_varname
            del self.zvars[old_varname]

            # Also rename in for the associated v.attribute(s)
            if old_varname in self.vattrs:
                self.vattrs[new_varname] = self.vattrs[old_varname]
                del self.vattrs[old_varname]

            return True

    def rm_zvar(self, varname):
        """
        Remove a zVariable from the Skeleton object.

        :param varname: name of the zVariable to remove
        :return:
        """
        logger.info("Removing zvariable {0}".format(varname))
        if varname in self.zvars:
            del self.zvars[varname]

        # Also remove associated v.attribute(s)
        if varname in self.vattrs:
            del self.vattrs[varname]

        self.header["nzvar"] -= 1
        return True

# ________________ Global Functions __________


# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)