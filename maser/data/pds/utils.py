#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python module to work with PDS Data
@author: B.Cecconi(LESIA)
"""

import os
import numpy

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2022, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "CeCILL"
__version__ = "1.0b4"
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

        def __init__(self, label_file, fmt_label_dict=None, verbose=False):
            super().__init__(self)
            self.verbose = verbose
            if fmt_label_dict is False:
                self.extra_labels = False
            else:
                self.extra_labels = True
            if fmt_label_dict is None:
                self.fmt_files = {}
            else:
                self.fmt_files = fmt_label_dict
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

            # If no input_file is set, retrieve current PDSLabelList file from self
            if input_file is None:
                input_file = self.file

            # Opening input_file and looping through lines
            with open(input_file, "r") as f:
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
                            if self.extra_labels:
                                fmt_file_name = cur_val.strip('"')
                                if fmt_file_name in self.fmt_files.keys():
                                    extra_file = self.fmt_files[fmt_file_name]
                                else:
                                    extra_file = os.path.join(
                                        os.path.dirname(input_file), fmt_file_name
                                    )
                                if self.verbose:
                                    print(
                                        "Inserting external Label from {}".format(
                                            extra_file
                                        )
                                    )
                                self._load_pds3_label_as_list(extra_file)
                            else:
                                if self.verbose:
                                    print("Skipping external Label.")

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

    def __init__(self, label_file, fmt_label_dict=None, verbose=False):

        super().__init__(self)
        self.verbose = verbose
        self.file = label_file
        if fmt_label_dict is None:
            self.fmt_files = {}
        else:
            self.fmt_files = fmt_label_dict
        label_list = self._PDSLabelList(self.file, self.fmt_files, self.verbose)
        self.process = label_list.process
        self._label_list_to_dict(label_list)

    def _label_list_to_dict(self, label_list):
        """This function transforms PDS3 Label list into a PDS3 Label dict"""

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


class PDSDataTableColumnHeader:
    def __init__(self, n_rows, column_label, verbose=False):
        self.verbose = verbose
        self.n_rows = n_rows
        self.label = column_label
        self.name = self.label["NAME"]

        if "ITEMS" in self.label.keys():
            self.n_items = int(self.label["ITEMS"])
        else:
            self.n_items = 1

        self.start_byte = int(self.label["START_BYTE"]) - 1

        self.bytes = int(self.label["BYTES"])

        if "ITEM_BYTES" in self.label.keys():
            self.item_bytes = self.label["ITEM_BYTES"]
        else:
            self.item_bytes = self.bytes

        self.struct_format = self._get_struct_format()
        if self.verbose:
            print(self.struct_format)

        self.np_data_type = self._get_np_data_type()
        if self.verbose:
            print(self.np_data_type)

    def _get_np_data_type(self):

        struct_to_np_data_type = {
            "b": numpy.int8,
            "B": numpy.uint8,
            "h": numpy.int16,
            "H": numpy.uint16,
            "i": numpy.int32,
            "I": numpy.uint32,
            "q": numpy.int64,
            "Q": numpy.uint64,
            "f": numpy.single,
            "d": numpy.float_,
            "c": numpy.str_,
        }
        return struct_to_np_data_type[self.struct_format[-1]]

    def _get_struct_format(self):

        data_type = ""
        endianess = ""

        if self.verbose:
            print("Data type = {}".format(self.label["DATA_TYPE"]))
            print("Item bytes= {}".format(self.item_bytes))

        if self.label["DATA_TYPE"].startswith("MSB"):
            endianess = ">"
        elif self.label["DATA_TYPE"].startswith("LSB"):
            endianess = "<"

        if self.label["DATA_TYPE"].endswith("INTEGER"):
            if int(self.item_bytes) == 1:
                data_type = "b"
            elif int(self.item_bytes) == 2:
                data_type = "h"
            elif int(self.item_bytes) == 4:
                data_type = "i"
            elif int(self.item_bytes) == 8:
                data_type = "q"
            elif self.label["DATA_TYPE"].startswith("ASCII"):
                data_type = "i"
        elif self.label["DATA_TYPE"].endswith("BIT_STRING"):
            data_type = "B"
            self.n_items = self.item_bytes
        elif (
            self.label["DATA_TYPE"].endswith("REAL")
            or self.label["DATA_TYPE"] == "FLOAT"
        ):
            data_type = "f"
            if self.label["DATA_TYPE"] == "PC_REAL":
                endianess = "<"
            else:
                endianess = ">"
        elif self.label["DATA_TYPE"] == "CHARACTER":
            data_type = "c"
            self.n_items = self.item_bytes
        else:
            raise ValueError(
                "Unknown (or not yet implemented) data type ({})".format(
                    self.label["DATA_TYPE"]
                )
            )

        if "UNSIGNED" in self.label["DATA_TYPE"]:
            data_type = data_type.upper()

        return "{}{}{}".format(endianess, self.n_items, data_type)

    def __repr__(self):
        return f"<PDSDataTableColumnHeader: {self.name}>"


class PDSDataTableObject(dict):
    def __init__(self, obj_label, data_file, data_offset=0, verbose=False):
        super().__init__(self)
        self.verbose = verbose
        self.filepath = data_file
        self.offset = data_offset
        self.label = obj_label
        self.n_columns = int(obj_label["COLUMNS"])
        self.n_rows = int(obj_label["ROWS"])
        self.columns = list()
        for col_label in obj_label["COLUMN"]:
            self.columns.append(
                PDSDataTableColumnHeader(self.n_rows, col_label, verbose=self.verbose)
            )
        self._create_data_structure()

    def _create_data_structure(self):
        # Setting up columns
        for cur_col in self.columns:

            if cur_col.n_items == 1:
                self[cur_col.name] = numpy.zeros(self.n_rows, cur_col.np_data_type)
            else:
                self[cur_col.name] = numpy.zeros(
                    (self.n_rows, cur_col.n_items), cur_col.np_data_type
                )

    def load_data(self):
        # Loading data into columns
        if self.label["INTERCHANGE_FORMAT"] == "ASCII":
            self._load_data_ascii()
        elif self.label["INTERCHANGE_FORMAT"] == "BINARY":
            self._load_data_binary()
        else:
            raise ValueError(
                "Unknown interchange format ({})".format(
                    self.label["INTERCHANGE_FORMAT"]
                )
            )

    def _load_data_ascii(self):
        with open(self.filepath, "r") as f:

            for ii, line in enumerate(f.readlines()):
                for cur_col in self.columns:
                    cur_name = cur_col.name
                    cur_byte_start = int(cur_col.start_byte)
                    cur_byte_length = int(cur_col.bytes)
                    if cur_col.n_items == 1:
                        if self.verbose:
                            print(
                                "Loading... {}[{}] from bytes {}:{}".format(
                                    cur_name,
                                    ii,
                                    cur_byte_start,
                                    cur_byte_start + cur_byte_length,
                                )
                            )
                        self[cur_name][ii] = line[
                            cur_byte_start : cur_byte_start + cur_byte_length
                        ]
                    else:
                        for cur_item in range(cur_col.n_items):
                            if self.verbose:
                                print(
                                    "Loading... {}[{}, {}] from bytes {}:{}".format(
                                        cur_name,
                                        ii,
                                        cur_item,
                                        cur_byte_start,
                                        cur_byte_start + cur_byte_length,
                                    )
                                )
                            self[cur_name][ii, cur_item] = line[
                                cur_byte_start : cur_byte_start + cur_byte_length
                            ]
                            cur_byte_start += cur_byte_length

    def _load_data_binary(self):

        import struct

        with open(self.filepath, "rb") as f:

            f.seek(self.offset)

            buf_length = int(self.label["ROW_BYTES"])
            if "ROW_PREFIX_BYTES" in self.label.keys():
                buf_length += int(self.label["ROW_PREFIX_BYTES"])
            if "ROW_SUFFIX_BYTES" in self.label.keys():
                buf_length += int(self.label["ROW_SUFFIX_BYTES"])

            for ii in range(self.n_rows):

                buf_data = f.read(buf_length)

                for cur_col in self.columns:
                    cur_name = cur_col.name
                    cur_byte_start = int(cur_col.start_byte)
                    cur_byte_length = int(cur_col.bytes)

                    if self.verbose:
                        print(
                            "Loading... {}[{}] from bytes {}:{} of buffer({} bytes) with format: {}".format(
                                cur_name,
                                ii,
                                cur_byte_start,
                                cur_byte_start + cur_byte_length,
                                buf_length,
                                cur_col.struct_format,
                            )
                        )

                    line = struct.unpack(
                        cur_col.struct_format,
                        buf_data[cur_byte_start : cur_byte_start + cur_byte_length],
                    )

                    if cur_col.n_items == 1:
                        self[cur_name][ii] = line[0]
                    else:
                        self[cur_name][ii, :] = line

    def __repr__(self):
        return f"<PDSTableObject: {self.label['NAME']} ({self.n_rows} rows x {self.n_columns} columns)>"
