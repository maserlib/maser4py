# -*- coding: utf-8 -*-
from typing import Union, List
from pathlib import Path

import numpy

from maser.data.base import BinData, VariableFrequencies
from .sweeps import (
    StereoWavesLfrL2HighResSweeps,
)
from astropy.time import Time
from astropy.units import Unit
from ..utils import _read_sweep_length, _merge_dtype, _read_block
from ..const import (
    CCSDS_CDS_FIELDS,
    CALDATE_FIELDS,
)

ANT_CFG_FIELDS = (
    [
        "ANT_CFG_1",
        "ANT_CFG_2",
        "ANT_CFG_3",
    ],
    ">hhh",
)


class StereoWavesL2HighResBinData(
    VariableFrequencies, BinData, dataset="cdpp_st__l2_wav_h_res"
):
    """Placeholder class for `cdpp_stX_l2_wav_XXX` binary data."""

    _iter_sweep_class = StereoWavesLfrL2HighResSweeps

    _dataset_keys = ["agc1", "agc2", "auto1", "auto2", "crossr", "crossi"]

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        BinData.__init__(self, filepath, dataset, access_mode)
        VariableFrequencies.__init__(self)
        self._data = None
        self._nsweep = None
        self._data = self._loader()
        self.fields = ["agc1", "agc2", "auto1", "auto2", "crossr", "crossi"]
        self.units = ["ADU", "ADU", "ADU", "ADU", "ADU", "ADU"]

    def _read_array_block(self, n1, n2):
        import struct

        nbytes = 4 * n1 * n2
        block = self.file.read(nbytes)
        data = struct.unpack(">" + "f" * (nbytes // 4), block)
        return numpy.array(data).reshape(n1, n2)

    def _loader(self, count_only=False):
        data = []
        nsweep = 0

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        caldate_fields, caldate_dtype = CALDATE_FIELDS
        ant_cfg_fields, ant_cfg_dtype = ANT_CFG_FIELDS

        header_fields = (
            ["RECEIVER_CODE"]
            + ccsds_fields
            + ["JULIAN_SEC"]
            + caldate_fields
            + [
                "JULIAN_SEC_FRAC",
                "INTEG_TIME",
                "NSTEP",
                "NFR_STEP",
                "NFREQ",
                "NCHANNEL",
            ]
            + ant_cfg_fields
            + [
                "NCONFIG",
                "NAGC2",
                "NAUTO2",
                "LOOP_A",
                "LOOP_C",
            ]
        )
        header_dtype = _merge_dtype(
            (">h", ccsds_dtype, ">L", caldate_dtype, ">ffhhhh", ant_cfg_dtype, ">hhhhh")
        )

        while True:
            try:
                # Reading number of bytes in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                nfreq = header_i["NFREQ"]
                nstep = header_i["NSTEP"]
                nconf = header_i["NCONFIG"]
                nauto1 = nfreq
                nauto2 = header_i["NAUTO2"]
                nagc1 = nstep
                nagc2 = header_i["NAGC2"]
                loopa = header_i["LOOP_A"]
                loopc = header_i["LOOP_C"]

                # Reading frequency list (kHz) in the current sweep
                cur_dtype = ">" + "f" * nfreq
                freq = _read_block(self.file, cur_dtype)

                # Reading time step table
                step_time = self._read_array_block(nstep, nconf)

                if self.load_data:

                    # Reading AGC1 table
                    agc1 = self._read_array_block(nagc1, nconf)

                    # Reading AGC2 table
                    if nagc2 == nstep:
                        agc2 = self._read_array_block(nagc2, nconf)
                    elif nagc2 == 0:
                        agc2 = None
                    else:
                        raise IOError("Corrupted file (inconsistent NAGC2 value)")

                    # Reading AUTO1 table
                    auto1 = self._read_array_block(nauto1, loopa)

                    # Reading AUTO2 table
                    if nauto2 == nfreq:
                        auto2 = self._read_array_block(nauto2, loopa)
                    elif nauto2 == 0:
                        auto2 = None
                    else:
                        raise IOError("Corrupted file (inconsistent NAUTO2 value)")

                    # Reading CROSS_R table
                    cross_r = self._read_array_block(nfreq, loopc)

                    # Reading CROSS_I table
                    cross_i = self._read_array_block(nfreq, loopc)

                    data_i = {
                        "freq": freq,
                        "step_time": step_time,
                        "agc1": agc1,
                        "agc2": agc2,
                        "auto1": auto1,
                        "auto2": auto2,
                        "cross_r": cross_r,
                        "cross_i": cross_i,
                    }
                else:
                    data_i = {
                        "freq": freq,
                        "step_time": step_time,
                    }
                    # Skip data section
                    self.file.seek(
                        4 * (nagc1 + nagc2) * nconf
                        + 4 * (nauto1 + nauto2) * loopa
                        + 4 * (2 * nfreq * loopc),
                        1,
                    )
                # Reading number of octets in the current sweep
                loctets2 = _read_sweep_length(self.file)
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break
            else:
                data.append({"hdr": header_i, "dat": data_i})
            nsweep += 1

        self._nsweep = nsweep // 3
        return data

    @property
    def times(self):
        if self._times is None:
            times = Time([], format="jd")
            for s in self.sweeps:
                k0 = list(s.header.keys())[0]
                times = numpy.append(
                    times,
                    Time(
                        f"{s.header[k0]['CALEND_DATE_YEAR']}-{s.header[k0]['CALEND_DATE_MONTH']}-"
                        f"{s.header[k0]['CALEND_DATE_DAY']} {s.header[k0]['CALEND_DATE_HOUR']}:"
                        f"{s.header[k0]['CALEND_DATE_MINUTE']}:{s.header[k0]['CALEND_DATE_SECOND']}"
                    ),
                )
            self._times = Time(times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies = []
            for s in self.sweeps:
                self._frequencies.append(s.data["freq"] * Unit("kHz"))
        return self._frequencies

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def quicklook(self, file_png=None, keys: Union[List[str], None] = None, **kwargs):
        if keys is None:
            keys = self.fields
        default_keys = self.fields
        db_tab = numpy.array([True, True, True, True, False, False])
        vmin_tab = numpy.array([-150, -160, -150, -160, -1, -1])
        vmax_tab = numpy.array([-120, -130, -120, -130, 1, 1])
        for qkey, tab in zip(["db", "vmin", "vmax"], [db_tab, vmin_tab, vmax_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)

        self._quicklook(
            keys=keys,
            file_png=file_png,
            y="frequency",
            # vmin=[-150, -160, -150, -160, -1, -1],
            # vmax=[-120, -130, -120, -130, 1, 1],
            # db=[True, True, True, True, False, False],
            **kwargs,
        )

    def epncore(self):
        md = BinData.epncore(self)
        md["obs_id"] = self.filepath.name
        # md["instrument_host_name"] = "interball-auroral"
        # md["instrument_name"] = "polrad"
        # md["target_name"] = "Earth"
        # md["target_class"] = "planet"
        # md["target_region"] = "magnetosphere"
        # md["feature_name"] = "AKR#Auroral Kilometric Radiation"

        # md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = numpy.min(self.frequencies * Unit("Hz"))
        md["spectral_range_max"] = numpy.max(self.frequencies * Unit("Hz"))

        # md["publisher"] = "CNES/CDPP"

        return md


class StereoAWavesL2HighResLfrBinData(
    StereoWavesL2HighResBinData,
    dataset="cdpp_sta_l2_wav_h_res_lfr",
):
    """CDPP STEREO-A Waves LFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_sta_l2_wav_h_res_lfr`
    - Data format: Binary"""


class StereoAWavesL2HighResHfrBinData(
    StereoWavesL2HighResBinData,
    dataset="cdpp_sta_l2_wav_h_res_hfr",
):
    """CDPP STEREO-A Waves HFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_sta_l2_wav_h_res_hfr`
    - Data format: Binary"""


class StereoBWavesL2HighResLfrBinData(
    StereoWavesL2HighResBinData,
    dataset="cdpp_stb_l2_wav_h_res_lfr",
):
    """CDPP STEREO-B Waves LFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_stb_l2_wav_h_res_lfr`
    - Data format: Binary"""


class StereoBWavesL2HighResHfrBinData(
    StereoWavesL2HighResBinData,
    dataset="cdpp_stb_l2_wav_h_res_hfr",
):
    """CDPP STEREO-B Waves HFR Level 2 High-Resolution dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_stb_l2_wav_h_res_hfr`
    - Data format: Binary"""
