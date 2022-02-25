# -*- coding: utf-8 -*-
from typing import Union, Dict
from pathlib import Path
from spacepy import pycdf
from astropy.io import fits
from maser.data.pds import PDSLabelDict
import numpy
from astropy.time import Time
from astropy.units import Unit


class BaseData:
    dataset: Union[None, str] = None
    _registry: Dict[str, "BaseData"] = {}

    def __init_subclass__(cls: "BaseData", *args, dataset: str, **kwargs) -> None:
        cls.dataset = dataset
        BaseData._registry[dataset] = cls

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ) -> None:
        self.filepath = filepath
        if access_mode not in ["sweeps", "records", "file"]:
            raise ValueError("Illegal access mode.")
        else:
            self.access_mode = access_mode
        self._file = None
        self._times = None
        self._frequencies = None

    @classmethod
    def get_dataset(cls, filepath):
        pass


class Data(BaseData, dataset="default"):
    def __new__(
        cls, filepath: Path, dataset: Union[None, str] = "__auto__", *args, **kwargs
    ) -> "Data":
        if dataset is None:
            # call the base data class __new__ method
            return super().__new__(cls)
        elif dataset == "__auto__":
            # try to guess the dataset
            dataset = cls.get_dataset(filepath)

            # get the dataset class from the registry
            DatasetClass = BaseData._registry[dataset]

            # create a new instance of the dataset class
            return DatasetClass(filepath, dataset=None, *args, **kwargs)
        else:
            # get the dataset class from the registry
            DatasetClass = BaseData._registry[dataset]

            # create a new instance of the dataset class
            return DatasetClass(filepath, dataset=None, *args, **kwargs)

    @classmethod
    def open(cls, filepath: Path, *args, **kwargs):
        return open(filepath, *args, **kwargs)

    @classmethod
    def close(cls, file):
        file.close()

    @property
    def file(self):
        if not self._file:
            self._file = self.open(self.filepath)
        return self._file

    @property
    def sweeps(self):
        yield

    @property
    def records(self):
        yield

    @property
    def meta(self) -> dict:
        return dict()

    @property
    def times(self):
        pass

    @property
    def frequencies(self):
        pass

    def as_array(self) -> numpy.ndarray:
        return numpy.ndarray(numpy.empty)

    def __enter__(self):
        if self.access_mode == "file":
            return self.file
        else:
            return self

    def __exit__(self, *args, **kwargs):
        if self._file:
            self.close(self._file)

    def __iter__(self):
        # get the reference to the right iterator (file, sweeps or records)
        ref = getattr(self, self.access_mode)
        for item in ref:
            yield item

    @staticmethod
    def get_dataset(filepath):
        if filepath.suffix.lower() == ".cdf":
            dataset = BaseData._registry["cdf"].get_dataset(filepath)
        elif filepath.suffix.lower() in [".fits", ".fit"]:
            dataset = BaseData._registry["fits"].get_dataset(filepath)
        elif filepath.suffix.lower() == ".lbl":
            dataset = BaseData._registry["pds3"].get_dataset(filepath)
        else:
            raise NotImplementedError()
        return dataset


class CdfData(Data, dataset="cdf"):
    @classmethod
    def open(cls, filepath: Path):
        return pycdf.CDF(str(filepath))

    @classmethod
    def get_dataset(cls, filepath):
        with cls.open(filepath) as c:
            dataset = c.attrs["Logical_source"][...][0]
        return dataset


class FitsData(Data, dataset="fits"):
    @classmethod
    def open(cls, filepath: Path):
        return fits.open(filepath)

    @classmethod
    def get_dataset(cls, filepath):
        with cls.open(filepath) as f:
            if f[0].header["INSTRUME"] == "NenuFar" and filepath.stem.endswith("_BST"):
                dataset = "nenufar_bst"
            elif "e-CALLISTO" in f[0].header["CONTENT"]:
                dataset = "ecallisto"
        return dataset


class Pds3Data(Data, dataset="pds3"):
    @classmethod
    def open(cls, filepath: Path):
        label = PDSLabelDict(filepath)
        data = None
        return {"label": label, "data": data}

    @classmethod
    def get_dataset(cls, filepath):
        file_label = cls.open(filepath)["label"]
        dataset = file_label["DATA_SET_ID"]
        return dataset

    @classmethod
    def close(cls, file):
        pass


class SrnNdaRoutineJupEdrCdfData(CdfData, dataset="srn_nda_routine_jup_edr"):
    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f["Frequency"][...] * Unit(
                    f["Frequency"].attrs["UNITS"]
                )
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f["Epoch"][...])
        return self._times


class NenufarBstFitsData(FitsData, dataset="nenufar_bst"):
    pass


class ECallistoFitsData(FitsData, dataset="ecallisto"):
    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = f[1].data["TIME"][0] * Unit("s") + Time(
                    f"{f[0].header['DATE-OBS'].replace('/', '-')} {f[0].header['TIME-OBS']}"
                )
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f[1].data["FREQUENCY"][0] * Unit("MHz")
        return self._frequencies


class Vg1JPra3RdrLowband6secV1Data(
    Pds3Data, dataset="VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    pass


if __name__ == "__main__":
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    print(type(data))
