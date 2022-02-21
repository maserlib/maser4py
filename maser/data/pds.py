#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python module to work with PDS Data
@author: B.Cecconi(LESIA)
"""

import os

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2022, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "CeCILL"
__version__ = "1.0b3"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Dev"
__date__ = "21-FEB-2022"
__project__ = "MASER/PADC PDS"


class PDSLabelDict(dict):
    """
    Class for the dict-form PDSLabel
    """

    class _PDSLabelList(list):
        """
        Class for the list-form PDSLabel (internal class, not accessible from outside)
        """

        def __init__(self, label_file, verbose=False, debug=False):

            if debug:
                print("### This is PDSLabelDict._PDSLabelList.__init__()")

            list.__init__(self)
            self.debug = debug
            self.verbose = verbose
            self.file = label_file
            self.process = list()
            self._load_pds3_label_as_list()
            self._merge_multiple_line_values()
            self._add_object_depth_to_label_list()
            if self.verbose:
                print(self.process)

        def _load_pds3_label_as_list(self, input_file=None):
            """
            This method loads label lines as pairs of (key, value) separated by "=", excluding comments.
            The method recursively loads any other .FMT files, for each ^STRUCTURE key.
            """

            if self.debug:
                print(
                    "### This is PDSLabelDict._PDSLabelList._load_pds3_label_as_list()"
                )

            # If no input_file is set, retrieve current PDSLabelList file from self
            if input_file is None:
                input_file = self.file

            # Opening input_file and looping through lines
            with open(input_file, "r") as f:

                if self.debug:
                    print("Reading from {}".format(input_file))

                for line in f.readlines():

                    if self.verbose:
                        print(line)

                    # if end of label file tag, then stop the loop
                    if line.strip() == "END":
                        break

                    # skipping comment lines and empty lines
                    elif line.startswith("/*") or line.strip() == "":
                        if self.verbose:
                            print("... skipping.")
                        continue

                    # processing "key = value" lines
                    elif "=" in line:
                        kv = line.strip().split("=")
                        cur_key = kv[0].strip()
                        cur_val = kv[1].strip().strip('"')
                        if self.verbose:
                            print("... key = {}, value = {}".format(cur_key, cur_val))

                        # in case of external FMT file, nested call to this function with the FMT file
                        if cur_key == "^STRUCTURE":
                            extra_file = os.path.join(
                                os.path.dirname(input_file), cur_val.strip('"')
                            )
                            if self.verbose:
                                print(
                                    "Inserting external Label from {}".format(
                                        extra_file
                                    )
                                )
                            self._load_pds3_label_as_list(extra_file)

                        # regular case: just write out a new line with (key, value)
                        else:
                            self.append((cur_key, cur_val))

                    # special case for multiple line values
                    else:
                        self.append(("", line.strip().strip('"')))

            self.process.append("Loaded from file")

        def _merge_multiple_line_values(self):
            """
            This method merges multiple line values
            """

            if self.debug:
                print(
                    "### This is PDSLabelDict._PDSLabelList._merge_multiple_line_values()"
                )

            prev_ii = 0
            remove_list = []

            # looping on Label list item, with enumerate, so that we get the item index in the list
            for ii, item in enumerate(self.__iter__()):
                (cur_key, cur_value) = item

                # in case of multiple line values, key is an empty string
                if cur_key == "":

                    # fetching last previous line with non empty key
                    (prev_key, prev_value) = self[prev_ii]
                    cur_value = "{} {}".format(prev_value, cur_value)

                    # appending current value to value of previous line with non empty key
                    self[prev_ii] = (prev_key, cur_value)

                    # flag the current line for deletion
                    remove_list.append(ii)

                # general case: non empty key
                else:
                    prev_ii = ii

            # remove lines flagged for deletion
            if len(remove_list) > 0:
                for ii in sorted(remove_list, reverse=True):
                    del self[ii]

            self.process.append("Merged multi line")

        def _add_object_depth_to_label_list(self):
            """Adds an extra elements after in each (key, value) containing the current object depth"""

            if self.debug:
                print(
                    "### This is PDSLabelDict._PDSLabelList._add_object_depth_to_label_list()"
                )

            depth = []
            remove_list = []

            for ii, item in enumerate(self.__iter__()):
                (cur_key, cur_value) = item

                # flag END_OBJECT line and removing the last element of the depth list
                if cur_key == "END_OBJECT":
                    remove_list.append(ii)
                    del depth[-1]

                # process other lines by adding the current version of the depth list
                else:
                    self[ii] = (cur_key, cur_value, depth.copy())

                    # when we meet an OBJECT line, add the object name to the depth list
                    if cur_key == "OBJECT":
                        depth.append(cur_value)

            # remove lines flagged for deletion
            if len(remove_list) > 0:
                for ii in sorted(remove_list, reverse=True):
                    del self[ii]

            self.process.append("Added depth tag")

    def __init__(self, label_file, verbose=False, debug=False):

        if debug:
            print("### This is PDSLabelDict.__init__()")

        dict.__init__(self)
        self.debug = debug
        self.verbose = verbose
        self.file = label_file
        label_list = self._PDSLabelList(self.file, self.verbose, self.debug)
        self.process = label_list.process
        self._label_list_to_dict(label_list)

    def _label_list_to_dict(self, label_list):
        """This function transforms PDS3 Label list into a PDS3 Label dict"""

        if self.debug:
            print("### This is PDSLabelDict._label_list_to_dict()")

        for item in label_list:
            (cur_key, cur_value, cur_depth) = item

            cur_dict = self
            if len(cur_depth) > 0:
                for cur_depth_item in cur_depth:
                    cur_dict = cur_dict[cur_depth_item][-1]

            if cur_key == "OBJECT":
                if self.verbose:
                    print("Creating {} Object".format(cur_value))
                if cur_value not in cur_dict.keys():
                    cur_dict[cur_value] = [dict()]
                else:
                    cur_dict[cur_value].append(dict())
            else:
                if self.verbose:
                    print(
                        "Inserting {} keyword with value {}".format(cur_key, cur_value)
                    )
                cur_dict[cur_key] = cur_value

        self.process.append("Converted to dict")
