# -*- coding: utf-8 -*-
from typing import Union, Dict
from pathlib import Path
from spacepy import pycdf
from astropy.io import fits
from maser.data.pds import PDSLabelDict


class BaseData:
    dataset: Union[None, str] = None
    _registry: Dict[str, "BaseData"] = {}

    def __init_subclass__(cls: "BaseData", *args, dataset: str, **kwargs) -> None:
        cls.dataset = dataset
        BaseData._registry[dataset] = cls

    def __init__(self, filepath: Path, dataset: Union[None, str] = "__auto__") -> None:
        self.filepath = filepath

    @staticmethod
    def get_dataset(filepath):
        pass


class Data(BaseData, dataset="default"):
    def __new__(cls, filepath: Path, dataset: Union[None, str] = "__auto__") -> "Data":
        if dataset is None:
            # call the base data class __new__ method
            return super().__new__(cls)
        elif dataset == "__auto__":
            # try to guess the dataset
            dataset = cls.get_dataset(filepath)

            # get the dataset class from the registry
            DatasetClass = BaseData._registry[dataset]

            # create a new instance of the dataset class
            return DatasetClass(filepath, dataset=None)
        else:
            # get the dataset class from the registry
            DatasetClass = BaseData._registry[dataset]

            # create a new instance of the dataset class
            return DatasetClass(filepath, dataset=None)

    @staticmethod
    def get_dataset(filepath):
        if filepath.suffix.lower() == ".cdf":
            dataset = BaseData._registry["cdf"].get_dataset(filepath)
        elif filepath.suffix.lower() == ".fits":
            dataset = BaseData._registry["fits"].get_dataset(filepath)
        elif filepath.suffix.lower() == ".lbl":
            dataset = BaseData._registry["pds3"].get_dataset(filepath)
        else:
            raise NotImplementedError()
        return dataset


class CdfData(Data, dataset="cdf"):
    @staticmethod
    def get_dataset(filepath):
        with pycdf.CDF(str(filepath)) as c:
            dataset = c.attrs["Logical_source"][...][0]
        return dataset


class FitsData(Data, dataset="fits"):
    @staticmethod
    def get_dataset(filepath):
        with fits.open(filepath) as f:
            if f[0].header["INSTRUME"] == "NenuFar" and filepath.stem.endswith("_BST"):
                dataset = "nenufar_bst"
        return dataset


class Pds3Data(Data, dataset="pds3"):
    @staticmethod
    def get_dataset(filepath):
        lbl = PDSLabelDict(filepath)
        dataset = lbl["DATA_SET_ID"]
        return dataset


class SrnNdaRoutineJupEdrCdfData(CdfData, dataset="srn_nda_routine_jup_edr"):
    pass


class NenufarBstFitsData(FitsData, dataset="nenufar_bst"):
    pass


class Vg1JPra3RdrLowband6secV1Data(
    Pds3Data, dataset="VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    pass


if __name__ == "__main__":
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    print(type(data))
