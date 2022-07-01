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


class PDSDataFromLabel:
    """
    This object contains PDS3 archive data, loaded from their label file.
    This is MaserDataFromFile object, based on the label file.
    Attributes:
        label: parsed label data mapped into a dictionary (PDSLabelDict object)
        pointers: dict containing {pointer_name: pointer_file} elements
        objects: list of object names (pointers to data files)
        dataset_name: name of PDS3 archive volume
        header: header info (depending on each volume)
        object: dict containing {object_name: MaserDataFromFile(object_file)} elements
    Methods:
        _decode_pointer(self, str_pointer)
        _detect_pointers(self)
        _detect_data_object_type(self)
        _fix_object_label_entries(self)
        load_data(self)
        get_single_sweep(self, index)
        get_first_sweep(self)
        get_last_sweep(self)
    """

    def __init__(
        self,
        file,
        label_dict=None,
        fmt_label_dict=None,
        load_data_input=True,
        verbose=False,
    ):

        if not file.lower().endswith(".lbl"):
            raise ValueError("Select label file instead of data file")

        self.verbose = verbose
        self.label_file = file
        self.format_labels = fmt_label_dict
        # self.PDSDataObject = data_object_class
        if label_dict is not None:
            self.label = label_dict
        else:
            self.label = PDSLabelDict(self.label_file, self.format_labels, verbose)
        self.pointers = self._detect_pointers()
        self.objects = self._detect_data_object_type()
        self.dataset_name = self.label["DATA_SET_ID"].strip('"')
        self._fix_object_label_entries()

        self.header = None
        self.time = None
        self.frequency = None
        self.object = {}

        self.load_data_flag = self._initialize_load_data_flag()
        self._update_load_data_flag(load_data_input)

        for cur_data_obj in self.objects:

            self.object[cur_data_obj] = self.PDSDataObject(
                self, self, self.label[cur_data_obj], cur_data_obj, self.verbose
            )

        self.load_data()

    def _initialize_load_data_flag(self):

        return dict(zip(self.objects, [False] * len(self.objects)))

    def _update_load_data_flag(self, load_data_input):

        if isinstance(load_data_input, bool):
            if load_data_input:
                for item in self.objects:
                    self.load_data_flag[item] = True
        elif isinstance(load_data_input, list):
            for item in load_data_input:
                if item in self.objects:
                    self.load_data_flag[item] = True
                else:
                    print(
                        "Warning object name unknown, can't load it. ({})".format(
                            str(item)
                        )
                    )
        elif isinstance(load_data_input, str):
            if load_data_input in self.objects:
                self.load_data_flag[load_data_input] = True
            else:
                print(
                    "Warning object name unknown, can't load it. ({})".format(
                        str(load_data_input)
                    )
                )
        else:
            print(
                "Warning object name(s) unknown, can't load it. ({})".format(
                    str(load_data_input)
                )
            )

    def _decode_pointer(self, str_pointer):
        dict_pointer = {}
        if str_pointer.startswith("("):
            str_pointer_tmp = str_pointer.strip()[1:-1].split(",")
            basename = str_pointer_tmp[0].strip('"')
            str_offset = str_pointer_tmp[1].strip()
            if str_offset.endswith("<BYTES>"):
                byte_offset = int(str_offset[:-7].strip()) - 1
            else:
                byte_offset = (int(str_offset.strip()) - 1) * int(
                    self.label["RECORD_BYTES"]
                )
        else:
            basename = str_pointer.strip().strip('"')
            byte_offset = 0

        dict_pointer["file_name"] = os.path.join(os.path.dirname(self.file), basename)
        dict_pointer["byte_offset"] = byte_offset

        return dict_pointer

    def _detect_pointers(self):
        pointers = {}
        for key in self.label.keys():
            if key.startswith("^"):
                pointers[key[1:]] = self._decode_pointer(self.label[key])
        return pointers

    def _detect_data_object_type(self):
        data_types = []
        for item in self.pointers.keys():
            if item in self.label.keys():
                data_types.append(item)
        return data_types

    def _fix_object_label_entries(self):
        for item in self.objects:
            self.label[item] = self.label[item][0]

    def load_data(self, data_object=None):
        if data_object is not None:
            self._update_load_data_flag(data_object)

        for cur_data_obj in self.objects:
            if (
                self.load_data_flag[cur_data_obj]
                and not self.object[cur_data_obj].data_loaded
            ):
                self.object[cur_data_obj].load_data()

    def _set_start_time(self):
        self.start_time = dateutil.parser.parse(self.label["START_TIME"], ignoretz=True)

    def _set_end_time(self):
        self.end_time = dateutil.parser.parse(self.label["STOP_TIME"], ignoretz=True)

    def get_single_sweep(self, index=0):
        pass

    def get_first_sweep(self):
        return self.get_single_sweep(0)

    def get_last_sweep(self):
        return self.get_single_sweep(-1)

    def get_freq_axis(self, unit=None):
        pass

    def get_time_axis(self):
        pass

    def get_mime_type(self):
        if self.object[self.objects[0]].label["INTERCHANGE_FORMAT"] == "ASCII":
            return "text/ascii"
        else:
            return MaserDataFromFile.get_mime_type(self)

    def get_epncore_meta(self):
        md = MaserDataFromFile.get_epncore_meta(self)
        md["granule_uid"] = ":".join(
            [self.label["DATA_SET_ID"], self.label["PRODUCT_ID"]]
        )
        md["granule_gid"] = self.label["DATA_SET_ID"]

        if "SPACECRAFT_NAME" in self.label.keys():
            md["instrument_host_name"] = self.label["SPACECRAFT_NAME"]
        elif "INSTRUMENT_HOST_NAME" in self.label.keys():
            md["instrument_host_name"] = self.label["INSTRUMENT_HOST_NAME"]

        if "INSTRUMENT_ID" in self.label.keys():
            md["instrument_name"] = self.label["INSTRUMENT_ID"]
        elif "INSTRUMENT_NAME" in self.label.keys():
            md["instrument_name"] = self.label["INSTRUMENT_NAME"]

        targets = {"name": set(), "class": set(), "region": set()}
        if "JUPITER" in self.label["TARGET_NAME"]:
            targets["name"].add("Jupiter")
            targets["class"].add("planet")
            targets["region"].add("magnetosphere")
        if "SATURN" in self.label["TARGET_NAME"]:
            targets["name"].add("Saturn")
            targets["class"].add("planet")
            targets["region"].add("magnetosphere")
        if "EARTH" in self.label["TARGET_NAME"]:
            targets["name"].add("Earth")
            targets["class"].add("planet")
            targets["region"].add("magnetosphere")
        if "NEPTUNE" in self.label["TARGET_NAME"]:
            targets["name"].add("Neptune")
            targets["class"].add("planet")
            targets["region"].add("magnetosphere")
        if "URANUS" in self.label["TARGET_NAME"]:
            targets["name"].add("Uranus")
            targets["class"].add("planet")
            targets["region"].add("magnetosphere")
        md["target_name"] = "#".join(targets["name"])
        md["target_class"] = "#".join(targets["class"])
        md["target_region"] = "#".join(targets["region"])

        md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = min(self.get_freq_axis(unit="Hz"))
        md["spectral_range_max"] = max(self.get_freq_axis(unit="Hz"))

        if "PRODUCT_CREATION_TIME" in self.label.keys():
            if self.label["PRODUCT_CREATION_TIME"] != "N/A":
                md["creation_date"] = dateutil.parser.parse(
                    self.label["PRODUCT_CREATION_TIME"], ignoretz=True
                )
                md["modification_date"] = dateutil.parser.parse(
                    self.label["PRODUCT_CREATION_TIME"], ignoretz=True
                )
                md["release_date"] = dateutil.parser.parse(
                    self.label["PRODUCT_CREATION_TIME"], ignoretz=True
                )

        md["publisher"] = "NASA/PDS/PPI"

        return md
