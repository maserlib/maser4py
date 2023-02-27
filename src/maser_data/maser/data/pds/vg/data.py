# -*- coding: utf-8 -*-
from ..data import Pds3Data
from maser.data.base import FixedFrequencies
from pathlib import Path
from typing import Union, List, Tuple
from ..utils import PDSDataTableObject
from .sweeps import VgPra3RdrLowband6secV1Sweeps
from astropy.time import Time
from astropy.units import Unit
import numpy


class VgPra3RdrLowband6secV1Data(
    FixedFrequencies,
    Pds3Data,
    dataset="VGX-X-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager 1 or 2 PRA Level 3 RDR LowBand
    6sec PDS3 dataset.
    """

    _iter_sweep_class = VgPra3RdrLowband6secV1Sweeps

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        Pds3Data.__init__(
            self,
            filepath,
            dataset,
            access_mode,
        )
        FixedFrequencies.__init__(self)

        self._nsweep = int(self.label["TABLE"]["ROWS"]) * 8
        self._sweep_length = 70
        self.table = PDSDataTableObject(
            self.label["TABLE"], self.pointers["TABLE"]["file_name"]
        )
        self.sweep_mapping: List[Tuple[int, int]] = []
        if self._load_data:
            self.load_data()
        self._data = self.table
        self._nrecord = self._nsweep * 8
        self.fields = ["R", "L"]
        self.units = [Unit("dB"), Unit("dB")]

    def load_data(self):
        self.table.load_data()
        self._load_data = True

        for isweep in range(self._nsweep):
            self.sweep_mapping.append((isweep // 8, isweep % 8))

    @staticmethod
    def _decode_date(cur_date):
        yy = cur_date // 10000
        if yy < 70:
            yy += 2000
        else:
            yy += 1900
        mm = (cur_date % 10000) // 100
        dd = cur_date % 100
        return f"{yy:04d}-{mm:02d}-{dd:02d}"

    @property
    def times(self):
        if self._times is None:
            times = Time(
                [self._decode_date(item) for item in self.table["DATE"]]
            ) + self.table["SECOND"] * Unit("s")
            self._times = Time(numpy.repeat(times, 8)) + (
                3.9 + 6 * (numpy.arange(self._nsweep) % 8)
            ) * Unit("s")
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies = numpy.arange(1326, -18, -19.2) * Unit("kHz")
        return self._frequencies

    def get_epncore_meta(self):
        md = Pds3Data.get_epncore_meta(self)
        md["granule_uid"] = f"{self.label['DATA_SET_ID']}:{self.label['PRODUCT_ID']}"
        md["granule_gid"] = self.label["DATA_SET_ID"]
        md["instrument_host_name"] = self.label.get(
            "SPACECRAFT_NAME", self.label.get("INSTRUMENT_HOST_NAME", None)
        )
        md["instrument_name"] = self.label.get(
            "INSTRUMENT_ID", self.label.get("INSTRUMENT_NAME", None)
        )

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

        md["spectral_range_min"] = min(self.frequencies.to(Unit("Hz")).value)
        md["spectral_range_max"] = max(self.frequencies.to(Unit("Hz")).value)

        if "PRODUCT_CREATION_TIME" in self.label.keys():
            if self.label["PRODUCT_CREATION_TIME"] != "N/A":
                md["creation_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso
                md["modification_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso
                md["release_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso

        md["publisher"] = "NASA/PDS/PPI"

        return md

    def as_xarray(self):
        import xarray

        fields = self.fields
        units = self.units
        fields.append("any")
        units.append("dB")

        datasets = {}
        for dataset_key, dataset_unit in zip(fields, units):
            data_arr = numpy.full((self._nsweep, self._sweep_length), numpy.nan)
            for i, sweep in enumerate(self.sweeps):
                if dataset_key == "any":
                    data_arr[i, :] = sweep.data.value
                else:
                    d = sweep[dataset_key]
                    data_arr[i, :] = numpy.repeat(d["data"].value, 2)

            datasets[dataset_key] = xarray.DataArray(
                data=data_arr,
                name=dataset_key,
                coords=[
                    ("time", self.times.to_datetime()),
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                ],
                attrs={"units": dataset_unit},
                dims=("time", "frequency"),
            )

        return datasets


class Vg1JPra3RdrLowband6secV1Data(
    VgPra3RdrLowband6secV1Data,
    dataset="VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager-1/PRA Jupiter Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2JPra3RdrLowband6secV1Data(
    VgPra3RdrLowband6secV1Data,
    dataset="VG2-J-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager-2/PRA Jupiter Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-J-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg1JPra4SummBrowse48secV1Data(
    Pds3Data, dataset="VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    pass


class Vg2JPra4SummBrowse48secV1Data(
    Pds3Data, dataset="VG2-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    pass


class Vg1SPra3RdrLowband6secV1Data(
    VgPra3RdrLowband6secV1Data, dataset="VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-1/PRA Saturn Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2SPra3RdrLowband6secV1Data(
    VgPra3RdrLowband6secV1Data, dataset="VG2-S-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-2/PRA Saturn Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-S-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2NPra2RdrHighrate60msV1Data(
    Pds3Data, dataset="VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1.0"
):
    pass


class Vg2NPra3RdrLowband6secV1Data(
    VgPra3RdrLowband6secV1Data, dataset="VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-2/PRA Neptune Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2UPra3RdrLowband6secV1Data(
    VgPra3RdrLowband6secV1Data, dataset="VG2-U-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-2/PRA Uranus Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-U-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass
