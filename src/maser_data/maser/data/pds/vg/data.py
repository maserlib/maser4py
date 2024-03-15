# -*- coding: utf-8 -*-
from ..data import Pds3DataTable, Pds3DataTimeSeries
from maser.data.base import FixedFrequencies
from pathlib import Path
from typing import Union, List, Tuple
from ..utils import PDSDataTableObject
from .sweeps import VgPra3RdrLowband6secV1Sweeps, VgPra4SummBrowse48secV1Sweeps
from astropy.time import Time
from astropy.units import Unit
import numpy

# ===================================================================
# VOYAGER-PRA-3-RDR-LOWBAND-6SEC datasets
# ===================================================================


class VgPra3RdrLowband6secV1Data(
    FixedFrequencies,
    Pds3DataTable,
    dataset="VGX-X-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager 1 or 2 PRA Level 3 RDR LowBand
    6sec PDS3 dataset.
    """

    _iter_sweep_class = VgPra3RdrLowband6secV1Sweeps
    _dataset_keys = None

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        Pds3DataTable.__init__(
            self,
            filepath,
            dataset,
            access_mode,
        )
        FixedFrequencies.__init__(self)

        self._nsweep = int(self.label["TABLE"]["ROWS"]) * 8
        self._sweep_length = 70
        self.table = PDSDataTableObject(
            self.label["TABLE"],
            self.pointers["TABLE"]["file_name"],
            data_set_id=self.label["DATA_SET_ID"],
            product_id=self.filepath.stem,
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
            self._times = Time([], format="jd")
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

    def epncore(self):
        md = Pds3DataTable.epncore(self)
        md["granule_uid"] = f"{self.label['DATA_SET_ID']}:{self.label['PRODUCT_ID']}"
        md["instrument_host_name"] = f"voyager-{self.label['DATA_SET_ID'][2]}"
        md["instrument_name"] = "pra#planetary-radio-astronomy"

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
        md["time_sampling_step_min"] = 6.0
        md["time_sampling_step_max"] = 6.0

        if "PRODUCT_CREATION_TIME" in self.label.keys():
            if self.label["PRODUCT_CREATION_TIME"] != "N/A":
                md["creation_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso
                md["modification_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso
                md["release_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso

        md["publisher"] = "NASA/PDS/PPI"

        return md

    @property
    def dataset_keys(self):
        if self._dataset_keys is None:
            self._dataset_keys = self.fields
            if "any" not in self._dataset_keys:
                self._dataset_keys.append("any")
        return self._dataset_keys

    def as_xarray(self):
        import xarray
        import warnings

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

            datasets[dataset_key] = (
                xarray.DataArray(
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
                .sortby("time")
                .T
            )
        warnings.warn(
            "WARNING: Time for Voyager are known for not being recorded in a not monotonic way. Be careful with these data."
        )

        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["L", "R"],
        **kwargs,
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )


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


# ===================================================================
# VOYAGER-PRA-4-SUMM-BROWSE-48SEC datasets
# ===================================================================


class VgPra4RSummBrowse48secV1Data(
    FixedFrequencies,
    Pds3DataTimeSeries,
    dataset="VGX-X-PRA-4-SUMM-BROWSE-48SEC-V1.0",
):
    """Class for the Voyager 1 or 2 PRA Level 4 Summary Browse
    48sec PDS3 dataset.
    """

    _iter_sweep_class = VgPra4SummBrowse48secV1Sweeps
    _dataset_keys = None

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        Pds3DataTimeSeries.__init__(
            self,
            filepath,
            dataset,
            access_mode,
        )
        FixedFrequencies.__init__(self)

        self._nsweep = int(self.label["TIME_SERIES"]["ROWS"])
        self._sweep_length = 70
        self.table = PDSDataTableObject(
            self.label["TIME_SERIES"],
            self.pointers["TIME_SERIES"]["file_name"],
            data_set_id=self.label["DATA_SET_ID"],
            product_id=self.filepath.stem,
        )
        self.sweep_mapping: List[Tuple[int, int]] = []
        if self._load_data:
            self.load_data()
        self._data = self.table
        self.fields = ["R", "L"]
        self.units = [Unit("dB"), Unit("dB")]

    def load_data(self):
        self.table.load_data()
        self._load_data = True

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            years = self.table["YEAR"] + 1900
            days = self.table["DAY"]
            hours = self.table["HOUR"]
            minutes = self.table["MINUTE"]
            seconds = self.table["SECOND"]
            self._times = Time(
                [
                    f"{yy}:{dd:03d}:{hh:02d}:{mm:02d}:{ss:02d}.000"
                    for yy, dd, hh, mm, ss in zip(
                        years,
                        days,
                        hours,
                        minutes,
                        seconds,
                    )
                ]
            )
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies = numpy.arange(1326, -18, -19.2) * Unit("kHz")
        return self._frequencies

    @property
    def dataset_keys(self):
        if self._dataset_keys is None:
            self._dataset_keys = self.fields
        return self._dataset_keys

    def as_xarray(self):
        import xarray

        fields = self.fields
        units = self.units

        datasets = {}
        for dataset_key, dataset_unit in zip(fields, units):
            data_arr = self.table[f"{dataset_key}H_DATA"] / 100

            datasets[dataset_key] = xarray.DataArray(
                data=data_arr.transpose(),
                name=dataset_key,
                coords=[
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                    ("time", self.times.to_datetime()),
                ],
                attrs={"units": dataset_unit},
                dims=("frequency", "time"),
            )

        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["L", "R"],
        **kwargs,
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )

    def epncore(self):
        md = Pds3DataTimeSeries.epncore(self)
        md["granule_uid"] = f"{self.label['DATA_SET_ID']}:{self.label['PRODUCT_ID']}"
        md["instrument_host_name"] = f"voyager-{self.label['DATA_SET_ID'][2]}"
        md["instrument_name"] = "pra#planetary-radio-astronomy"

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
        md["time_sampling_step_min"] = 48.0
        md["time_sampling_step_max"] = 48.0

        if "PRODUCT_CREATION_TIME" in self.label.keys():
            if self.label["PRODUCT_CREATION_TIME"] != "N/A":
                md["creation_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso
                md["modification_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso
                md["release_date"] = Time(self.label["PRODUCT_CREATION_TIME"]).iso

        md["publisher"] = "NASA/PDS/PPI"

        return md


class Vg1JPra4SummBrowse48secV1Data(
    VgPra4RSummBrowse48secV1Data, dataset="VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-1/PRA Jupiter Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


class Vg2JPra4SummBrowse48secV1Data(
    VgPra4RSummBrowse48secV1Data, dataset="VG2-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-2/PRA Jupiter Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-J-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


class Vg2NPra4SummBrowse48secV1Data(
    VgPra4RSummBrowse48secV1Data, dataset="VG2-N-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-2/PRA Neptune Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-N-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


class Vg2UPra4SummBrowse48secV1Data(
    VgPra4RSummBrowse48secV1Data, dataset="VG2-U-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-2/PRA Uranus Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-U-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


# ===================================================================
# VOYAGER-PRA-2-RDR-HIHRATE-60MS datasets
# ===================================================================


class Vg2NPra2RdrHighrate60msV1Data(
    Pds3DataTable, dataset="VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1.0"
):
    pass
