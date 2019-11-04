#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS Data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "GPLv3"
__version__ = "1.0b2"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "28-FEB-2018"
__project__ = "MASER/PADC PDS"

__all__ = ["PDSDataFromLabel", "PDSDataObject", "PDSDataATableObject", "PDSDataTableObject", "PDSError", "PDSDataTimeSeriesObject",
           "PDSLabelDict"]

import dateutil.parser
import os
import numpy
from maser.data import MaserDataFromFile, MaserError
from astropy.table import Table


class PDSLabelDict(dict):
    """
    Class for the dict-form PDSLabel
    """

    class _PDSLabelList(list):
        """
        Class for the list-form PDSLabel (internal class, not accessible from outside)
        """

        def __init__(self, label_file, fmt_label_dict=None, verbose=False, debug=False):

            if debug:
                print("### This is PDSLabelDict._PDSLabelList.__init__()")

            list.__init__(self)
            self.debug = debug
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

            if self.debug:
                print("### This is PDSLabelDict._PDSLabelList._load_pds3_label_as_list()")

            # If no input_file is set, retrieve current PDSLabelList file from self
            if input_file is None:
                input_file = self.file

            # Opening input_file and looping through lines
            with open(input_file, 'r') as f:

                if self.debug:
                    print("Reading from {}".format(input_file))

                for line in f.readlines():

                    if self.verbose:
                        print(line)

                    # if end of label file tag, then stop the loop
                    if line.strip() == "END":
                        break

                    # skipping comment lines and empty lines
                    elif line.startswith('/*') or line.strip() == '':
                        if self.verbose:
                            print("... skipping.")
                        continue

                    # processing "key = value" lines
                    elif '=' in line:
                        kv = line.strip().split('=')
                        cur_key = kv[0].strip()
                        cur_val = kv[1].strip().strip('"')
                        if self.verbose:
                            print("... key = {}, value = {}".format(cur_key, cur_val))

                        # in case of external FMT file, nested call to this function with the FMT file
                        if cur_key == '^STRUCTURE':
                            fmt_file_name = cur_val.strip('"')
                            if fmt_file_name in self.fmt_files.keys():
                                extra_file = self.fmt_files[fmt_file_name]
                            else:
                                extra_file = os.path.join(os.path.dirname(input_file), fmt_file_name)
                            if self.verbose:
                                print("Inserting external Label from {}".format(extra_file))
                            self._load_pds3_label_as_list(extra_file)

                        # regular case: just write out a new line with (key, value)
                        else:
                            self.append((cur_key, cur_val))

                    # special case for multiple line values
                    else:
                        self.append(("", line.strip().strip('"')))

            self.process.append('Loaded from file')

        def _merge_multiple_line_values(self):
            """
            This method merges multiple line values
            """

            if self.debug:
                print("### This is PDSLabelDict._PDSLabelList._merge_multiple_line_values()")

            prev_ii = 0
            remove_list = []

            # looping on Label list item, with enumerate, so that we get the item index in the list
            for ii, item in enumerate(self.__iter__()):
                (cur_key, cur_value) = item

                # in case of multiple line values, key is an empty string
                if cur_key == '':

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

            self.process.append('Merged multi line')

        def _add_object_depth_to_label_list(self):
            """Adds an extra elements after in each (key, value) containing the current object depth"""

            if self.debug:
                print("### This is PDSLabelDict._PDSLabelList._add_object_depth_to_label_list()")

            depth = []
            remove_list = []

            for ii, item in enumerate(self.__iter__()):
                (cur_key, cur_value) = item

                # flag END_OBJECT line and removing the last element of the depth list
                if cur_key == 'END_OBJECT':
                    remove_list.append(ii)
                    del depth[-1]

                # process other lines by adding the current version of the depth list
                else:
                    self[ii] = (cur_key, cur_value, depth.copy())

                    # when we meet an OBJECT line, add the object name to the depth list
                    if cur_key == 'OBJECT':
                        depth.append(cur_value)

            # remove lines flagged for deletion
            if len(remove_list) > 0:
                for ii in sorted(remove_list, reverse=True):
                    del self[ii]

            self.process.append('Added depth tag')

    def __init__(self, label_file, fmt_label_dict=None, verbose=False, debug=False):
        """This class is used to store PDS3 label information in a Dictionary structure.

        It takes a PDS3 label file as the main input. If extra label files (such as .FMT files) are required to decode
        the data, the `fmt_label_dict` parameter is used to pass a dictionary containing the series of FMT label files,
        with the FMT name as keys and the FMT label file as values.

        Example:
        ```fmt_files = {
            'LRFULL_TABLE': '../FMT/LRFULL_TABLE.FMT',
            'RPWS_SCLK_SCET': '../FMT/RPWS_SCLK_SCET.FMT',
            'LRFC_DATA_QUALITY': '../FMT/LRFC_DATA_QUALITY.FMT'
            }
        lbl = PDSLabelDict('T2000366_HFR0.LBL', fmt_label_dict=fmt_files)
        ```

        :param label_file (str): Input PDS3 label file
        :param fmt_label_dict (dict): Extra FMT label files dictionary
        :param verbose (bool): Verbose flag (default: False)
        :param debug (bool): Debug flag (default: False)
        """

        if debug:
            print("### This is PDSLabelDict.__init__()")

        dict.__init__(self)
        self.debug = debug
        self.verbose = verbose
        self.file = label_file
        if fmt_label_dict is None:
            self.fmt_files = {}
        else:
            self.fmt_files = fmt_label_dict
        label_list = self._PDSLabelList(self.file, self.fmt_files, self.verbose, self.debug)
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

            if cur_key == 'OBJECT':
                if self.verbose:
                    print('Creating {} Object'.format(cur_value))
                if cur_value not in cur_dict.keys():
                    cur_dict[cur_value] = [dict()]
                else:
                    cur_dict[cur_value].append(dict())
            else:
                if self.verbose:
                    print('Inserting {} keyword with value {}'.format(cur_key, cur_value))
                cur_dict[cur_key] = cur_value

        self.process.append('Converted to dict')


class PDSError(MaserError):
    pass


class PDSDataObject(MaserDataFromFile):

    def __init__(self, product, parent, obj_label, obj_name, verbose=False, debug=False):

        if debug:
            print("### This is PDSDataObject.__init__()")

        self.verbose = verbose
        self.debug = debug
        self.product = product
        self.parent = parent
        self.obj_type = obj_name
        self.label = obj_label
        data_file = product.pointers[obj_name]['file_name']
        MaserDataFromFile.__init__(self, data_file, verbose, debug)
        self.data = None
        self.data_offset_in_file = product.pointers[obj_name]['byte_offset']
        self.data_loaded = False

    def data_from_object_type(self):

        if self.debug:
            print("### This is PDSDataObject.data_from_object_type()")

        pass

    def load_data(self):

        if self.debug:
            print("### This is PDSDataObject.load_data()")

        self.data.load_data()
        self.data_loaded = True


class PDSDataFromLabel(MaserDataFromFile):
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

    def __init__(self, file, label_dict=None, fmt_label_dict=None, load_data_input=True,
                 data_object_class=PDSDataObject, verbose=False, debug=False):

        if debug:
            print("### This is PDSDataFromLabel.__init__()")

        if not file.lower().endswith('.lbl'):
            raise PDSError('Select label file instead of data file')

        self.debug = debug
        self.verbose = verbose
        self.label_file = file
        self.format_labels = fmt_label_dict
        MaserDataFromFile.__init__(self, file, verbose, debug)
        self.PDSDataObject = data_object_class
        if label_dict is not None:
            self.label = label_dict
        else:
            self.label = PDSLabelDict(self.label_file, self.format_labels, verbose, debug)
        self.pointers = self._detect_pointers()
        self.objects = self._detect_data_object_type()
        self.dataset_name = self.label['DATA_SET_ID'].strip('"')
        self._fix_object_label_entries()

        self.header = None
        self.time = None
        self.frequency = None
        self.object = {}

        self.load_data_flag = self._initialize_load_data_flag()
        self._update_load_data_flag(load_data_input)

        for cur_data_obj in self.objects:

            if self.debug:
                print("Processing object: {}".format(cur_data_obj))

            self.object[cur_data_obj] = self.PDSDataObject(
                self, self, self.label[cur_data_obj], cur_data_obj,
                self.verbose, self.debug)

            if self.debug:
                print("Loading data into object: {}".format(cur_data_obj))

        self.load_data()

    def _initialize_load_data_flag(self):

        if self.debug:
            print("### This is PDSDataFromLabel._initialize_load_data_flag()")

        return dict(zip(self.objects, [False] * len(self.objects)))

    def _update_load_data_flag(self, load_data_input):

        if self.debug:
            print("### This is PDSDataFromLabel._update_load_data_flag()")

        if isinstance(load_data_input, bool):
            if load_data_input:
                for item in self.objects:
                    self.load_data_flag[item] = True
        elif isinstance(load_data_input, list):
            for item in load_data_input:
                if item in self.objects:
                    self.load_data_flag[item] = True
                else:
                    print("Warning object name unknown, can't load it. ({})".format(str(item)))
        elif isinstance(load_data_input, str):
            if load_data_input in self.objects:
                self.load_data_flag[load_data_input] = True
            else:
                print("Warning object name unknown, can't load it. ({})".format(str(load_data_input)))
        else:
            print("Warning object name(s) unknown, can't load it. ({})".format(str(load_data_input)))

    def _decode_pointer(self, str_pointer):

        if self.debug:
            print("### This is PDSDataFromLabel._decode_pointer()")

        dict_pointer = {}
        if str_pointer.startswith("("):
            str_pointer_tmp = str_pointer.strip()[1:-1].split(',')
            basename = str_pointer_tmp[0].strip('"')
            str_offset = str_pointer_tmp[1].strip()
            if str_offset.endswith('<BYTES>'):
                byte_offset = int(str_offset[:-7].strip())-1
            else:
                byte_offset = (int(str_offset.strip())-1) * int(self.label['RECORD_BYTES'])
        else:
            basename = str_pointer.strip().strip('"')
            byte_offset = 0

        dict_pointer['file_name'] = os.path.join(os.path.dirname(self.file), basename)
        dict_pointer['byte_offset'] = byte_offset

        return dict_pointer

    def _detect_pointers(self):

        if self.debug:
            print("### This is PDSDataFromLabel._detect_pointers()")

        pointers = {}
        for key in self.label.keys():
            if key.startswith('^'):
                pointers[key[1:]] = self._decode_pointer(self.label[key])

        if self.debug:
            print("Pointer(s) found: {}".format(', '.join(list(pointers.keys()))))

        return pointers

    def _detect_data_object_type(self):

        if self.debug:
            print("### This is PDSDataFromLabel._detect_data_object_type()")

        data_types = []
        for item in self.pointers.keys():
            if item in self.label.keys():
                data_types.append(item)

        if self.debug:
            print("Data type(s) found: {}".format(', '.join(data_types)))

        return data_types

    def _fix_object_label_entries(self):

        if self.debug:
            print("### This is PDSDataFromLabel._fix_object_label_entries()")

        for item in self.objects:
            self.label[item] = self.label[item][0]

    def load_data(self, data_object=None):

        if self.debug:
            print("### This is PDSDataFromLabel.load_data()")

        if data_object is not None:
            self._update_load_data_flag(data_object)

        for cur_data_obj in self.objects:
            if self.load_data_flag[cur_data_obj] and not self.object[cur_data_obj].data_loaded:
                self.object[cur_data_obj].load_data()

    def _set_start_time(self):
        self.start_time = dateutil.parser.parse(self.label['START_TIME'], ignoretz=True)

    def _set_end_time(self):
        self.end_time = dateutil.parser.parse(self.label['STOP_TIME'], ignoretz=True)

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
        if self.object[self.objects[0]].label['INTERCHANGE_FORMAT'] == 'ASCII':
            return 'text/ascii'
        else:
            return MaserDataFromFile.get_mime_type(self)

    def get_epncore_meta(self):
        md = MaserDataFromFile.get_epncore_meta(self)
        md['granule_uid'] = ":".join([self.label['DATA_SET_ID'], self.label['PRODUCT_ID']])
        md['granule_gid'] = self.label['DATA_SET_ID']

        if 'SPACECRAFT_NAME' in self.label.keys():
            md['instrument_host_name'] = self.label['SPACECRAFT_NAME']
        elif 'INSTRUMENT_HOST_NAME' in self.label.keys():
            md['instrument_host_name'] = self.label['INSTRUMENT_HOST_NAME']

        if 'INSTRUMENT_ID' in self.label.keys():
            md['instrument_name'] = self.label['INSTRUMENT_ID']
        elif 'INSTRUMENT_NAME' in self.label.keys():
            md['instrument_name'] = self.label['INSTRUMENT_NAME']

        targets = {'name': set(), 'class': set(), 'region': set()}
        if 'JUPITER' in self.label['TARGET_NAME']:
            targets['name'].add('Jupiter')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        if 'SATURN' in self.label['TARGET_NAME']:
            targets['name'].add('Saturn')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        if 'EARTH' in self.label['TARGET_NAME']:
            targets['name'].add('Earth')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        if 'NEPTUNE' in self.label['TARGET_NAME']:
            targets['name'].add('Neptune')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        if 'URANUS' in self.label['TARGET_NAME']:
            targets['name'].add('Uranus')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        md['target_name'] = '#'.join(targets['name'])
        md['target_class'] = '#'.join(targets['class'])
        md['target_region'] = '#'.join(targets['region'])

        md['dataproduct_type'] = 'ds'

        md['spectral_range_min'] = min(self.get_freq_axis(unit='Hz'))
        md['spectral_range_max'] = max(self.get_freq_axis(unit='Hz'))

        if 'PRODUCT_CREATION_TIME' in self.label.keys():
            if self.label['PRODUCT_CREATION_TIME'] != 'N/A':
                md['creation_date'] = dateutil.parser.parse(self.label['PRODUCT_CREATION_TIME'], ignoretz=True)
                md['modification_date'] = dateutil.parser.parse(self.label['PRODUCT_CREATION_TIME'], ignoretz=True)
                md['release_date'] = dateutil.parser.parse(self.label['PRODUCT_CREATION_TIME'], ignoretz=True)

        md['publisher'] = 'NASA/PDS/PPI'

        return md


class PDSDataTableColumnHeaderObject:
    def __init__(self, product, parent, column_label, verbose=False, debug=False):
        self.verbose = verbose
        self.debug = debug
        self.product = product
        self.parent = parent
        self.n_rows = parent.n_rows
        self.label = column_label
        self.name = self.label['NAME']

        if 'ITEMS' in self.label.keys():
            self.n_items = int(self.label['ITEMS'])
        else:
            self.n_items = 1

        self.start_byte = int(self.label['START_BYTE']) - 1

        self.bytes = int(self.label['BYTES'])

        if 'ITEM_BYTES' in self.label.keys():
            self.item_bytes = self.label['ITEM_BYTES']
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
            'b': numpy.int8,
            'B': numpy.uint8,
            'h': numpy.int16,
            'H': numpy.uint16,
            'i': numpy.int32,
            'I': numpy.uint32,
            'q': numpy.int64,
            'Q': numpy.uint64,
            'f': numpy.single,
            'd': numpy.float_,
            'c': numpy.str_
        }
        return struct_to_np_data_type[self.struct_format[-1]]

    def _get_struct_format(self):

        data_type = ''
        endianess = ''

        if self.verbose:
            print("Data type = {}".format(self.label['DATA_TYPE']))
            print("Item bytes= {}".format(self.item_bytes))

        if self.label['DATA_TYPE'].startswith('MSB'):
            endianess = '>'
        elif self.label['DATA_TYPE'].startswith('LSB'):
            endianess = '<'

        if self.label['DATA_TYPE'].endswith('INTEGER'):
            if int(self.item_bytes) == 1:
                data_type = 'b'
            elif int(self.item_bytes) == 2:
                data_type = 'h'
            elif int(self.item_bytes) == 4:
                data_type = 'i'
            elif int(self.item_bytes) == 8:
                data_type = 'q'
            elif self.label['DATA_TYPE'].startswith('ASCII'):
                data_type = 'i'
        elif self.label['DATA_TYPE'].endswith('BIT_STRING'):
            data_type = 'B'
            self.n_items = self.item_bytes
        elif self.label['DATA_TYPE'].endswith('REAL') or self.label['DATA_TYPE'] == 'FLOAT':
            data_type = 'f'
            if self.label['DATA_TYPE'] == 'PC_REAL':
                endianess = '<'
            else:
                endianess = '>'
        elif self.label['DATA_TYPE'] == 'CHARACTER':
            data_type = 'c'
            self.n_items = self.item_bytes
        else:
            raise PDSError('Unknown (or not yet implemented) data type ({})'.format(self.label['DATA_TYPE']))

        if 'UNSIGNED' in self.label['DATA_TYPE']:
            data_type = data_type.upper()

        return '{}{}{}'.format(endianess, self.n_items, data_type)


class PDSDataATableObject:

    def __init__(self, product, parent, obj_label, verbose=False, debug=False):

        if debug:
            print("### This is PDSDataATableObject.__init__()")

        self.verbose = verbose
        self.debug = debug
        self.product = product
        self.parent = parent
        self.label = obj_label
        self.n_columns = int(obj_label['COLUMNS'])
        self.n_rows = int(obj_label['ROWS'])
        self.columns = list()
        for col_label in obj_label['COLUMN']:
            self.columns.append(PDSDataTableColumnHeaderObject(self.product, self, col_label,
                                                               verbose=verbose, debug=debug))

        self.table = Table()

    def load_data(self):

        from .const import PDS_UNITS

        dt = []
        void_index = 0

        prev_stop_byte = 0
        for cur_col in self.columns:

            # adding void data columns when necessary
            if prev_stop_byte != cur_col.start_byte:
                dt.append(('void{}'.format(void_index), 'S{}'.format(cur_col.start_byte - prev_stop_byte)))
                void_index += 1

            if cur_col.np_data_type == numpy.str_:
                dt.append((cur_col.name, '|S{}'.format(cur_col.n_items)))
            else:
                dt.append((cur_col.name, cur_col.struct_format))

            prev_stop_byte = cur_col.start_byte + cur_col.bytes

        self.table = Table(numpy.fromfile(self.parent.file, numpy.dtype(dt)))

        # removing void data columns
        for col_name in self.table.keys():
            if col_name.startswith('void'):
                self.table.remove_column(col_name)

        # striping spaces in string columns
        for col_name in self.table.keys():
            if self.table[col_name].dtype.str.startswith('|S'):
                self.table[col_name] = numpy.char.strip(self.table[col_name])

        # bytes to unicode
        for col_name in self.table.keys():
            if self.table[col_name].dtype.str.startswith('|S'):
                self.table[col_name] = numpy.char.decode(self.table[col_name])

        # adding units when available:
        for cur_col in self.columns:
            if 'UNIT' in cur_col.label.keys():
                self.table[cur_col.name].unit = PDS_UNITS[cur_col.label['UNIT']]


class PDSDataTableObject(dict):

    def __init__(self, product, parent, obj_label, verbose=False, debug=False):

        if debug:
            print("### This is PDSDataTableObject.__init__()")

        dict.__init__(self)
        self.verbose = verbose
        self.debug = debug
        self.product = product
        self.parent = parent
        self.label = obj_label
        self.n_columns = int(obj_label['COLUMNS'])
        self.n_rows = int(obj_label['ROWS'])
        self.columns = list()
        for col_label in obj_label['COLUMN']:
            self.columns.append(PDSDataTableColumnHeaderObject(self.product, self, col_label,
                                                               verbose=verbose, debug=debug))
        self._create_data_structure()

    def _create_data_structure(self):

        if self.debug:
            print("### This is PDSDataTableObject._create_data_structure()")

        # Setting up columns
        for cur_col in self.columns:

            if cur_col.n_items == 1:
                self[cur_col.name] = numpy.zeros(self.n_rows, cur_col.np_data_type)
            else:
                self[cur_col.name] = numpy.zeros((self.n_rows, cur_col.n_items), cur_col.np_data_type)

            if self.debug:
                print("Column {} shape = {}".format(cur_col.name, str(numpy.shape(self[cur_col.name]))))

    def load_data(self):

        if self.debug:
            print("### This is PDSDataTableObject.load_data()")

        # Loading data into columns
        if self.label['INTERCHANGE_FORMAT'] == 'ASCII':
            self._load_data_ascii()
        elif self.label['INTERCHANGE_FORMAT'] == 'BINARY':
            self._load_data_binary()
        else:
            raise PDSError('Unknown interchange format ({})'.format(self.label['INTERCHANGE_FORMAT']))

    def _load_data_ascii(self):

        if self.debug:
            print("### This is PDSDataTableObject._load_data_ascii()")
            print("Starting ASCII read from {}".format(self.parent.file))

        with open(self.parent.file, 'r') as f:

            for ii, line in enumerate(f.readlines()):
                for cur_col in self.columns:
                    cur_name = cur_col.name
                    cur_byte_start = int(cur_col.start_byte)
                    cur_byte_length = int(cur_col.bytes)
                    if cur_col.n_items == 1:
                        if self.verbose:
                            print("Loading... {}[{}] from bytes {}:{}".format(cur_name, ii, cur_byte_start,
                                                                              cur_byte_start + cur_byte_length))
                        self[cur_name][ii] = line[cur_byte_start:cur_byte_start + cur_byte_length]
                    else:
                        for cur_item in range(cur_col.n_items):
                            if self.verbose:
                                print("Loading... {}[{}, {}] from bytes {}:{}".format(cur_name, ii, cur_item,
                                                                                      cur_byte_start,
                                                                                      cur_byte_start + cur_byte_length))
                            self[cur_name][ii, cur_item] = line[cur_byte_start:cur_byte_start + cur_byte_length]
                            cur_byte_start += cur_byte_length

    def _load_data_binary(self):

        import struct

        if self.debug:
            print("### This is PDSDataTableObject._load_data_binary()")
            print("Starting BINARY read from {}".format(self.parent.file))

        with open(self.parent.file, 'rb') as f:

            f.seek(self.parent.data_offset_in_file)

            buf_length = int(self.label['ROW_BYTES'])
            if 'ROW_PREFIX_BYTES' in self.label.keys():
                buf_length += int(self.label['ROW_PREFIX_BYTES'])
            if 'ROW_SUFFIX_BYTES' in self.label.keys():
                buf_length += int(self.label['ROW_SUFFIX_BYTES'])

            for ii in range(self.n_rows):

                buf_data = f.read(buf_length)

                for cur_col in self.columns:
                    cur_name = cur_col.name
                    cur_byte_start = int(cur_col.start_byte)
                    cur_byte_length = int(cur_col.bytes)

                    if self.verbose:
                        print(
                            "Loading... {}[{}] from bytes {}:{} of buffer({} bytes) with format: {}".format(
                                cur_name, ii, cur_byte_start, cur_byte_start + cur_byte_length,
                                buf_length, cur_col.struct_format))

                    line = struct.unpack(
                        cur_col.struct_format, buf_data[cur_byte_start:cur_byte_start + cur_byte_length])

                    if cur_col.n_items == 1:
                        self[cur_name][ii] = line[0]
                    else:
                        self[cur_name][ii, :] = line


class PDSDataTimeSeriesObject(PDSDataTableObject):

    def __init__(self, product, parent, obj_label, verbose=True, debug=False):

        if debug:
            print("### This is PDSDataTimeSeriesObject.__init__()")

        PDSDataTableObject.__init__(self, product, parent, obj_label, verbose=verbose, debug=debug)
        self.time_sampling = {"interval": self.label['SAMPLING_PARAMETER_INTERVAL'],
                              'unit': self.label['SAMPLING_PARAMETER_UNIT']}
