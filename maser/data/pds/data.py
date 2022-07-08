# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union
from maser.data.base import Data
from .utils import PDSLabelDict


class Pds3Data(Data, dataset="pds3"):
    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
        fmt_label_dict=None,
    ):
        super().__init__(filepath, dataset, access_mode)
        self.label = PDSLabelDict(self.filepath, fmt_label_dict)
        self.pointers = self._detect_pointers()
        self.objects = self._detect_data_object_type()
        self._fix_object_label_entries()

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

        dict_pointer["file_name"] = self.filepath.parent.resolve() / basename
        dict_pointer["byte_offset"] = byte_offset
        dict_pointer["object_type"] = "table"

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

    @classmethod
    def open_label(cls, filepath: Path, fmt_label_dict=None):
        return PDSLabelDict(filepath, fmt_label_dict=fmt_label_dict)

    @classmethod
    def open_data(cls, filepath: Path):
        pass

    @classmethod
    def open(cls, filepath: Path, *args, fmt_label_dict=None, **kwargs):
        # ignore 'gets multiple values for keyword argument "fmt_label_dict"'
        label = cls.open_label(filepath, *args, fmt_label_dict=fmt_label_dict, **kwargs)  # type: ignore
        data = None
        return {"label": label, "data": data}

    @classmethod
    def get_dataset(cls, filepath):
        file_label = cls.open_label(filepath, fmt_label_dict=False)
        return file_label["DATA_SET_ID"].strip('"')

    @classmethod
    def close(cls, file):
        pass


class Pds3DataTable(Pds3Data, dataset="pds3-table"):
    pass
