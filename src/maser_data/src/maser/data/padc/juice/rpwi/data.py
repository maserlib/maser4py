# -*- coding: utf-8 -*-

"""Classes for JUICE/RPWI datasets"""

from maser.data.base import CdfData, FixedFrequencies

# from maser.data.base.sweeps import Sweeps, Sweep

from typing import Union, List
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit
from .sweeps import JuiceCdfDataSweeps


"""
class JuiceCdfDataSweep(Sweep):
    def __init__(self, header, data, time, frequencies):
        super().__init__(header, data)
        self._time = time
        self._frequencies = frequencies


class JuiceCdfDataSweeps(Sweeps):
    @property
    def generator(self):
        frequencies = self.data_reference.frequencies

        # Convert the data to XArray
        xdata = self.data_reference.as_xarray()

        for i, time in enumerate(self.data_reference.times):
            yield ExpresCdfDataSweep(
                header={"header_keyword": "x-array generate data"},
                data={datakey: xdata[datakey].isel(time=[i]) for datakey in xdata},
                time=time,
                frequencies=frequencies,
            )


class JuiceRPWIhfL1aRAWSweeps(Sweeps):
    @property
    def generator(self):
        # attrs = self.file["Eu_i"].attrs
        for t, deui, deuq, devi, devq, dewi, dewq in zip(
            self.data_reference.times,
            # {self.file[key][...] for key in ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]},
            self.file["Eu_i"][...],
            self.file["Eu_q"][...],
            self.file["Ev_i"][...],
            self.file["Ev_q"][...],
            self.file["Ew_i"][...],
            self.file["Ew_q"][...],
            ):
            yield (
                t,
                self.data_reference.frequencies,
                [
                    deui[...] * Unit(""),  # units are raw in L1a
                    deuq[...] * Unit(""),
                    devi[...] * Unit(""),
                    devq[...] * Unit(""),
                    dewi[...] * Unit(""),
                    dewq[...] * Unit(""),
                ]
                # d[...] * Unit(attrs["UNITS"]),  # units are raw in L1a
            )


class JuiceRPWIhfL1aFULLSweeps(Sweeps):
    @property
    def generator(self):
        # attrs = self.file["Eu_i"].attrs
        for t, deueu, deuevim, deuevre, devev, devewim, devewre, dewew, deweuim, deweure in zip(
            self.data_reference.times,
            self.file["EuEu"][...],
            self.file["EuEv_im"][...],
            self.file["EuEv_re"][...],
            self.file["EvEv"][...],
            self.file["EvEw_im"][...],
            self.file["EvEw_re"][...],
            self.file["EwEw"][...],
            self.file["EwEu_im"][...],
            self.file["EwEu_re"][...],
            ):
            yield (
                t,
                self.data_reference.frequencies,
                [
                    deueu[...] * Unit(""),  # units are raw in L1a
                    deuevim[...] * Unit(""),
                    deuevre[...] * Unit(""),
                    devev[...] * Unit(""),
                    devewim[...] * Unit(""),
                    devewre[...] * Unit(""),
                    dewew[...] * Unit(""),
                    deweuim[...] * Unit(""),
                    deweure[...] * Unit(""),
                ]
                # d[...] * Unit(attrs["UNITS"]),  # units are raw in L1a
            )


class JuiceRPWIhfL1aPOLSEPSweeps(Sweeps):
    @property
    def generator(self):
        # attrs = self.file["Eu_i"].attrs
        for t, deueu_nc, deuevim_nc, deuevre_nc, devev_nc, devewim_nc, devewre_nc, dewew_nc, deweuim_nc, deweure_nc,
        deueu_nc, deuevim_nc, deuevre_nc, devev_nc, devewim_nc, devewre_nc, dewew_nc, deweuim_nc, deweure_nc,
        deueu_nc, deuevim_nc, deuevre_nc, devev_nc, devewim_nc, devewre_nc, dewew_nc, deweuim_nc, deweure_nc in zip(
            self.data_reference.times,
            self.file["EuEu_NC"][...],
            self.file["EuEv_im_NC"][...],
            self.file["EuEv_re_NC"][...],
            self.file["EvEv_NC"][...],
            self.file["EvEw_im_NC"][...],
            self.file["EvEw_re_NC"][...],
            self.file["EwEw_NC"][...],
            self.file["EwEu_im_NC"][...],
            self.file["EwEu_re_NC"][...],
            self.file["EuEu_LC"][...],
            self.file["EuEv_im_LC"][...],
            self.file["EuEv_re_LC"][...],
            self.file["EvEv_LC"][...],
            self.file["EvEw_im_LC"][...],
            self.file["EvEw_re_LC"][...],
            self.file["EwEw_LC"][...],
            self.file["EwEu_im_LC"][...],
            self.file["EwEu_re_LC"][...],
            self.file["EuEu_RC"][...],
            self.file["EuEv_im_RC"][...],
            self.file["EuEv_re_RC"][...],
            self.file["EvEv_RC"][...],
            self.file["EvEw_im_RC"][...],
            self.file["EvEw_re_RC"][...],
            self.file["EwEw_RC"][...],
            self.file["EwEu_im_RC"][...],
            self.file["EwEu_re_RC"][...],
            ):
            yield (
                t,
                self.data_reference.frequencies,
                [
                    deueu[...] * Unit(""),  # units are raw in L1a
                    deuevim[...] * Unit(""),
                    deuevre[...] * Unit(""),
                    devev[...] * Unit(""),
                    devewim[...] * Unit(""),
                    devewre[...] * Unit(""),
                    dewew[...] * Unit(""),
                    deweuim[...] * Unit(""),
                    deweure[...] * Unit(""),
                ]
                # d[...] * Unit(attrs["UNITS"]),  # units are raw in L1a
            )
"""


class JuiceRPWIhfL1CdfData(CdfData, FixedFrequencies, dataset="jui_rpwi_hf_l1_"):  # type: ignore
    """Class for `rpwi-hf` L1 (a and b) CDF files."""

    _iter_sweep_class = JuiceCdfDataSweeps

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
                name=self.file[dataset_key].attrs["LABLAXIS"],
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
        keys: Union[List[str], None] = None,
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

    # _iter_sweep_class = JuiceRPWIhfL1aRAWSweeps
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

    _dataset_keys = ["EE"]
    _display_keys = ["EE"]
    _db_disp = [True]


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
    # raise NotImplementedError()


class JuiceRPWIhfL1aCdfSID22(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID22"):
    """Class for `rpwi-hf` L1a SID22 CDF files."""

    _dataset_keys = ["auto_corr"]
    _display_keys = ["auto_corr"]
    _db_disp = [True]
    # raise NotImplementedError()


class JuiceRPWIhfL1aCdfSID7(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID7"):
    """Class for `rpwi-hf` L1a SID7 CDF files."""

    _dataset_keys = ["auto_corr"]
    _display_keys = ["auto_corr"]
    _db_disp = [True]
    # raise NotImplementedError()


class JuiceRPWIhfL1aCdfSID23(JuiceRPWIhfL1aCdf, dataset="JUICE_L1a_RPWI-HF-SID23"):
    """Class for `rpwi-hf` L1a SID23 CDF files."""

    _dataset_keys = ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]
    _display_keys = ["Eu_i", "Eu_q", "Ev_i", "Ev_q", "Ew_i", "Ew_q"]
    _db_disp = [True, True, True, True, True, True]
    # raise NotImplementedError()


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
