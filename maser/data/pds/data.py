# -*- coding: utf-8 -*-
from maser.data.base import Data
from pathlib import Path
from .utils import PDSLabelDict


class Pds3Data(Data, dataset="pds3"):
    @classmethod
    def open_label(cls, filepath: Path, fmt_label_dict=None):
        return PDSLabelDict(filepath, fmt_label_dict=fmt_label_dict)

    @classmethod
    def open_data(cls, filepath: Path):
        pass

    @classmethod
    def open(cls, filepath: Path, fmt_label_dict=None):
        label = cls.open_label(filepath, fmt_label_dict=fmt_label_dict)
        data = None
        return {"label": label, "data": data}

    @classmethod
    def get_dataset(cls, filepath):
        file_label = cls.open_label(filepath, fmt_label_dict=False)
        return file_label["DATA_SET_ID"]

    @classmethod
    def close(cls, file):
        pass


class Pds3DataTable(Pds3Data, dataset="pds3-table"):
    pass
