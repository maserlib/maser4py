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


    def is_valid_header(self, header):
        """
        Check that the input is a valid cdf header.

        :param header: header dictionary
        :return: True if the header is valid
        """

        for entry in header:
            for field in SHEETS[HEADER]:
                if field not in entry:
                    logger.error("{0} field is missing!".format(field))
                    return False

        return True

    def is_valid_gatt(self, entries):
        """
        Check that the input is a valid gattrs entry.

        :param entries:
        :return: True if it is valid
        """
        for entry in entries:
            for field in SHEETS[GATTRS]:
                if field not in entry:
                    logger.error("{0} field is missing!".format(field))
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
                logger.error("{0} field is missing!".format(field))
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
                    logger.error("{0} field is missing!".format(field))
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

    def add_gattr(self, attname, entries,
                  append=False):
        """
        Add a global attribute to the Skeleton object.


        :param attname: name of the g. attribute to add
        :param entries: List containing the entries for the g.attribute
        :param append: If True, then append input entries to the existing one
        """

        logger.info("Adding g.attribute {0}".format(attname))
        if attname in self.gattrs and append:
            # Check that all the expected fields are in the input entries
            if not self.is_valid_gatt(entries):
                raise InvalidEntry

            # Get number of entries
            nentry = len(self.gattrs[attname])
            for i, entry in enumerate(entries):
                entry["Entry Number"] = str(nentry + 1)
                self.gattrs[attname].append(entry)

        elif attname in self.gattrs:
            logger.warning("{0} already exists!".format(attname))
        else:
            # Check that all the expected fields are in the input entries
            if not self.is_valid_gatt(entries):
                raise InvalidEntry

            self.gattrs[attname] = entries


    def set_gattr(self, attname, entries, auto_add=False):
        """
        Update entries for a given g.attribute in the Skeleton object.

        :param attname: name of the g.attribute to update
        :param entries: new entries
        :param auto_add: If g.attribute does not exist, then add it with the input entries
        :return:
        """
        logger.info("Updating g.attribute {0}".format(attname))
        # Check if the attribute already exists
        if attname not in self.gattrs:
            if not auto_add:
                logger.error(
                    "{0} g.attribute does not exist!".format(
                    attname))
                raise IOError
            else:
                self.add_gattr(attname, entries)
                return True

        if len(entries) > len(self.gattrs[attname]):
            logger.error("Number of input entries is inconsistent!")
            raise InvalidEntry

        for i, entry in enumerate(entries):
            for key, val in entry.items():
                if key not in SHEETS[GATTRS]:
                    logger.warning("Unknown field: {0}!".format(key))
                    continue
                self.gattrs[attname][i][key] = val

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
            raise IOError
        else:
            self.gattrs[new_attname] = self.gattrs[old_attname]
            del self.gattrs[old_attname]

            if old_attname in self.vattrs:
                self.gattrs[new_attname] = self.gattrs[old_attname]
                del self.gattrs[old_attname]



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


    def add_vattr(self, attname, entry, varname=None):
        """
        Add a variable attribute into the Skeleton object.

        :param attname: name of the v. attribute to add
        :param entry: List containing the entry for the v.attribute
        :param varname: If provided, contains a list of zvariable for which the v.attribute must be added. If not provided v.attribute is added for all the variables.
        :return:
        """
        logger.info("Adding v.attribute {0}".format(attname))
        if attname in self.vattrList:
            logger.warning("{0} already exists!".format(attname))
        else:
            # Check that all the expected fields are in the input entries
            if not self.is_valid_vattrs(entry):
                raise InvalidEntry

            self.vattrList.append(attname)

            if not varname:
                varname = self.vattrs.keys()
            else:
                for var in varname:
                    if var not in self.vattrs:
                        logger.error("{0} not found!".format(var))
                        raise InvalidEntry

            for zvar in varname:
                self.vattrs[zvar][attname] = entry


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
            raise IOError
        else:
            if not self.is_valid_vattrs(entry):
                raise InvalidEntry

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
            raise IOError
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

        ;param varname: name of the zVariable to add
        :param entry: list with fields to add [variable name, data type, number elements,
                    dims, sizes, record variance, Dimension variances]. If dims=0, sizes and record variance must be None
        :param vattrs: dictionnary containing variable attribute(s) to load for this zvariable
        :return:
        """
        logger.info("Adding zvariable {0}".format(varname))
        # Check if the zVariable already exists
        if varname in self.zvars:
            logger.warning(
                           "{0} variable already exists!".format(
                                                        varname))
        else:
            # Check content
            if not self.is_valid_zvar(entry):
                raise InvalidEntry
            # Add the zvariable
            self.zvars[varname] = entry

            if vattrs:
                if not self.is_valid_vattr(vattrs):
                    raise InvalidEntry

                self.vattrs[varname] = vattrs

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
            raise IOError
        else:
            # update the zvariable

            for field in SHEETS[ZVARS]:
                if field in entry:
                    self.zvars[varname][field] = entry[field]
                else:
                    continue

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
            raise IOError
        else:
            self.zvars[new_varname] = self.zvars[old_varname]
            del self.zvars[old_varname]

            # Also rename in for the associated v.attribute(s)
            if old_varname in self.vattrs:
                self.vattrs[new_varname] = self.vattrs[old_varname]
                del self.vattrs[old_varname]

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



# ________________ Global Functions __________



# _________________ Main ____________________________
if __name__ == "__main__":
    print(__file__)