# -*- coding: utf-8 -*-

"""Classes for Sorbet datasets"""

from maser.data.base import CdfData

from typing import Union, List
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit


class JuiceRPWIhfL1CdfData(CdfData, dataset="jui_rpwi_hf_l1_"):  # type: ignore
    """Class for `rpwi-hf` L1 (a and b) CDF files."""

    def __init_subclass__(cls, *args, dataset: str, **kwargs) -> None:
        return super().__init_subclass__(*args, dataset=dataset, **kwargs)

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            with self.open(self.filepath) as f:
                self._times = Time(f["Epoch"][...])
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                # self._frequencies = f["frequency"][...] * Unit(
                self._frequencies = f["frequency"][...][0, :-1] * Unit(
                    f["frequency"].attrs["UNITS"]
                )
        return self._frequencies

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        import xarray

        dataset_keys = self.dataset_keys
        datasets = {}

        for dataset_key in dataset_keys:
            datasets[dataset_key] = xarray.DataArray(
                data=self.file[dataset_key][...].T[:-1, :],
                # name=self.file[dataset_key].attrs["LABLAXIS"],
                coords=[
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                    ("time", self.times.to_datetime()),
                ],
                dims=("frequency", "time"),
                attrs={
                    "units": self.file[dataset_key].attrs["UNITS"],
                    "title": self.file[dataset_key].attrs["CATDESC"],
                },
            ).sortby("frequency")
        return xarray.Dataset(data_vars=datasets)


class JuiceRPWIhfL1aCdf(JuiceRPWIhfL1CdfData, dataset="JUICE_L1a_RPWI-HF-SID_"):
    """Class for `rpwi-hf` L1a CDF files."""

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        yscale: str = "log",
        keys: List[str] = None,
        **kwargs,
    ):
        if keys is None:
            keys = self._display_keys

        self._quicklook(
            keys=keys,
            file_png=file_png,
            # landscape=landscape,
            db=self._db_disp,
            yscale=yscale,
            **kwargs,
        )


class JuiceRPWIhfL1aCdfSID2(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID2"):
    """Class for `rpwi-hf` L1a SID2 CDF files."""

    _dataset_keys = ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]
    _display_keys = ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]
    _db_disp = [True, True, True, True, True, True]


class JuiceRPWIhfL1aCdfSID3(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID3"):
    """Class for `rpwi-hf` L1a SID3 CDF files."""

    _dataset_keys = ["EuEu", "EvEv", "EwEw"]
    _display_keys = ["EuEu", "EvEv", "EwEw"]
    _db_disp = [True, True, True]


class JuiceRPWIhfL1aCdfSID4(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID4"):
    """Class for `rpwi-hf` L1a SID4 CDF files."""

    _dataset_keys = ["EuEu", "EvEv", "EwEw"]
    _display_keys = ["EuEu", "EvEv", "EwEw"]
    _db_disp = [True, True, True]


class JuiceRPWIhfL1aCdfSID20(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID20"):
    """Class for `rpwi-hf` L1a SID20 CDF files."""

    _dataset_keys = ["EuEu", "EvEv", "EwEw"]
    _display_keys = ["EuEu", "EvEv", "EwEw"]
    _db_disp = [True, True, True]


class JuiceRPWIhfL1aCdfSID5(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID5"):
    """Class for `rpwi-hf` L1a SID5 CDF files."""

    _dataset_keys = ["EuEu", "EvEv", "EwEw"]
    _display_keys = ["EuEu", "EvEv", "EwEw"]
    _db_disp = [True, True, True]


class JuiceRPWIhfL1aCdfSID21(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID21"):
    """Class for `rpwi-hf` L1a SID21 CDF files."""

    _dataset_keys = ["EuEu", "EvEv", "EwEw"]
    _display_keys = ["EuEu", "EvEv", "EwEw"]
    _db_disp = [True, True, True]


class JuiceRPWIhfL1aCdfSID6(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID6"):
    """Class for `rpwi-hf` L1a SID6 CDF files."""

    _dataset_keys = ["auto_corr"]
    _display_keys = ["auto_corr"]
    _db_disp = [True]


class JuiceRPWIhfL1aCdfSID22(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID22"):
    """Class for `rpwi-hf` L1a SID22 CDF files."""

    _dataset_keys = ["auto_corr"]
    _display_keys = ["auto_corr"]
    _db_disp = [True]


class JuiceRPWIhfL1aCdfSID7(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID7"):
    """Class for `rpwi-hf` L1a SID7 CDF files."""

    _dataset_keys = ["auto_corr"]
    _display_keys = ["auto_corr"]
    _db_disp = [True]


class JuiceRPWIhfL1aCdfSID23(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID23"):
    """Class for `rpwi-hf` L1a SID23 CDF files."""

    _dataset_keys = ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]
    _display_keys = ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]
    _db_disp = [True, True, True, True, True, True]


class JuiceRPWIhfL1bCdf(JuiceRPWIhfL1CdfData, dataset="JUICE_L1b_RPWI-HF-SID3"):
    """Class for `rpwi-hf` L1b CDF files."""

    _dataset_keys = [
        "EuEu",
    ]

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        yscale: str = "log",
        keys: List[str] = [
            "EuEu",
        ],
        **kwargs,
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # landscape=landscape,
            # db=[True,True],
            yscale=yscale,
            **kwargs,
        )
