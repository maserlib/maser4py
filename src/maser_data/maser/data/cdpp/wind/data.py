# -*- coding: utf-8 -*-
from typing import Union, List
from pathlib import Path
from maser.data.base import BinData, RecordsOnly, VariableFrequencies
from .sweeps import (
    WindWavesL260sSweeps,
    WindWavesL2HighResSweeps,
    WindWaves60sSweeps,
)
from .records import WindWavesTnrL3Bqt1mnRecords
from astropy.time import Time
from astropy.units import Unit
from ..utils import _read_sweep_length, _merge_dtype, _read_block
from ..const import (
    CCSDS_CDS_FIELDS,
    CALDATE_FIELDS,
    ORBIT_FIELDS,
)
import numpy as np


class WindWavesRad1L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v2"):
    """CDPP Wind Waves RAD1 Level 2 60s-Average (version 2) dataset

    - Observatory/Facility: WIND
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_wi_wa_rad1_l2_60s_v2`
    - Data format: Binary"""

    _iter_sweep_class = WindWavesL260sSweeps


class WindWavesL2BinData(VariableFrequencies, BinData, dataset="cdpp_wi_wa_l2"):
    """Placeholder class for `cdpp_wi_wa_XXX_l2` binary data."""

    _iter_sweep_class = WindWavesL2HighResSweeps

    _dataset_keys = ["VSPAL", "VZPAL", "TSPAL", "TZPAL"]

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
        self.fields = ["VS", "VSP", "VZ", "TS", "TSP", "TZ"]
        self.units = ["uV2/Hz", "uV2/Hz", "uV2/Hz", "s", "s", "s"]

    @property
    def _parse_file_name(self):
        pieces = self.filepath.stem.split("_")
        return dict(
            zip(
                ["facility", "instrument", "receiver", "level", "date", "version"],
                ["wind", "waves", pieces[2], pieces[3], pieces[4], pieces[5]],
            )
        )

    def _read_data_block(self, nbytes):
        import struct

        block = self.file.read(nbytes)
        Vspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        block = self.file.read(nbytes)
        Tspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        return np.array(Vspal, dtype=float), np.array(Tspal, dtype=float)

    def _loader(self, count_only=False):
        data = []
        nsweep = 0

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        caldate_fields, caldate_dtype = CALDATE_FIELDS
        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + [
                "JULIAN_SEC_FRAC",
                "ISWEEP",
                "IUNIT",
                "NPBS",
                "SUN_ANGLE",
                "SPIN_RATE",
                "KSPIN",
                "MODE",
                "LISTFR",
                "NFREQ",
                "ICAL",
                "IANTEN",
                "IPOLA",
                "IDIPXY",
                "SDURCY",
                "SDURPA",
                "NPALCY",
                "NFRPAL",
                "NPALIF",
                "NSPALF",
                "NZPALF",
            ]
        )
        header_dtype = _merge_dtype(
            (ccsds_dtype, ">hL", caldate_dtype, ">fihhffhhhhhhhhffhhhhh")
        )

        while True:
            try:
                # Reading number of bytes in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                npalf = header_i["NPALIF"]
                nspal = header_i["NSPALF"]
                nzpal = header_i["NZPALF"]

                # Reading frequency list (kHz) in the current sweep
                cur_dtype = ">" + "f" * npalf
                freq = np.array(_read_block(self.file, cur_dtype), dtype=float)

                if self.load_data:
                    # Reading intensity and time values for S/SP in the current sweep
                    Vspal, Tspal = self._read_data_block(4 * npalf * nspal)
                    # Reading intensity and time values for Z in the current sweep
                    Vzpal, Tzpal = self._read_data_block(4 * npalf * nzpal)

                    # Get indices of S and SP channels
                    index_s = (2 * np.arange(nspal / 2)).astype(int)
                    index_sp = (2 * np.arange(nspal / 2) + 1).astype(int)

                    # Reshape Vspal, Tspal, Vzpal, Tzpal into 2D arrays
                    Vspal = Vspal.reshape((nspal, npalf))
                    Vzpal = Vzpal.reshape((nzpal, npalf))
                    Tspal = Tspal.reshape((nspal, npalf))
                    Tzpal = Tzpal.reshape((nzpal, npalf))

                    data_i = {
                        "FREQ": np.tile(freq, (nzpal, 1)),
                        "VS": np.take(Vspal, index_s, axis=0),
                        "VSP": np.take(Vspal, index_sp, axis=0),
                        "VZ": Vzpal,
                        "TS": np.take(Tspal, index_s, axis=0),
                        "TSP": np.take(Tspal, index_sp, axis=0),
                        "TZ": Tzpal,
                    }

                else:
                    # Skip data section
                    self.file.seek(8 * npalf * (nspal + nzpal), 1)
                    data_i = None
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

        self._nsweep = nsweep
        return data

    @property
    def max_sweep_length(self):
        if self._max_sweep_length is None:
            self._max_sweep_length = np.max(
                [len(f.flatten()) for f in self.frequencies]
            )
        return self._max_sweep_length

    def as_xarray(self):
        import xarray

        fields = self.fields
        units = self.units

        freq_arr = np.full((self._nsweep, self.max_sweep_length), np.nan)

        for i in range(self._nsweep):
            f = self.frequencies[i].value.flatten()
            freq_arr[i, : len(f)] = f
            freq_arr[i, len(f) :] = f[-1]

        freq_index = range(self.max_sweep_length)

        datasets = {}
        for dataset_key, dataset_unit in zip(fields, units):
            data_arr = np.full((self._nsweep, self.max_sweep_length), np.nan)
            for i, sweep in enumerate(self.sweeps):
                d = sweep.data[dataset_key].flatten()
                data_arr[i, : len(d)] = d

            datasets[dataset_key] = xarray.DataArray(
                data=data_arr.T,
                name=dataset_key,
                coords={
                    "freq_index": freq_index,
                    "time": self.times.to_datetime(),
                    "frequency": (["time", "freq_index"], freq_arr, {"units": "kHz"}),
                },
                attrs={"units": dataset_unit},
                dims=("freq_index", "time"),
            )

        return xarray.Dataset(data_vars=datasets)

    @property
    def times(self):
        import numpy

        if self._times is None:
            times = Time([], format="jd")
            for s in self.sweeps:
                header = s.header
                times = numpy.append(
                    times,
                    Time(
                        f"{header['CALEND_DATE_YEAR']}-{header['CALEND_DATE_MONTH']}-"
                        f"{header['CALEND_DATE_DAY']} {header['CALEND_DATE_HOUR']}:"
                        f"{header['CALEND_DATE_MINUTE']}:{header['CALEND_DATE_SECOND']}"
                    ),
                )
            self._times = Time(times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies = []
            for s in self.sweeps:
                self._frequencies.append(s.data["FREQ"] * Unit("kHz"))
        return self._frequencies

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def quicklook(self, file_png=None, keys: List[str] = ["VSPAL", "VZPAL"], **kwargs):
        self._quicklook(
            file_png=file_png,
            keys=keys,
            **kwargs,
        )

    def epncore(self):
        md = BinData.epncore(self)
        md["granule_uid"] = f"{self.dataset}:{self.filepath.stem}"
        md[
            "obs_id"
        ] = f"wi_wa_{self._parse_file_name['receiver']}_{self._parse_file_name['date']}"

        md["instrument_host_name"] = "wind"
        md["instrument_name"] = "waves"
        md["target_name"] = "Earth#Sun"
        md["target_class"] = "planet#star"
        md["target_region"] = "magnetosphere#heliopshere"
        md[
            "feature_name"
        ] = "AKR#Auroral Kilometric Radiation#Solar bursts#Type II#Type III"

        md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = min(
            [min(item.to("Hz").value) for item in self.frequencies]
        )
        md["spectral_range_max"] = max(
            [max(item.to("Hz").value) for item in self.frequencies]
        )

        md["publisher"] = "CNES/CDPP"
        return md


class WindWavesRad1L2BinData(WindWavesL2BinData, dataset="cdpp_wi_wa_rad1_l2"):
    """Class for `cdpp_wi_wa_rad1_l2` binary data."""

    pass


class WindWavesRad2L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad2_l2_60s_v2"):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL260sV2BinData(BinData, dataset="cdpp_wi_wa_tnr_l2_60s_v2"):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL3Bqt1mnBinData(
    RecordsOnly, BinData, dataset="cdpp_wi_wa_tnr_l3_bqt_1mn"
):
    """Class for `cdpp_wi_wa_tnr_l3_bqt_1mn` data."""

    _iter_record_class = WindWavesTnrL3Bqt1mnRecords

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "records",
        load_data: bool = True,
    ) -> None:
        super().__init__(filepath, dataset, access_mode, load_data)


class WindWavesTnrL3NnBinData(BinData, dataset="cdpp_wi_wa_tnr_l3_nn"):
    """Class for `cdpp_wi_wa_tnr_l3_nn` data."""

    pass


class WindWavesL260sV1BinData(BinData, dataset="cdpp_wi_wa___l2_60s_v1"):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    _iter_sweep_class = WindWaves60sSweeps

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        super().__init__(filepath, dataset, access_mode, fixed_frequencies=False)
        self._data = None
        self._nsweep = None
        self.__max_sweep_length = None
        self._data = self._loader()

    def _loader(self):
        data = []

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS

        caldate_fields, caldate_dtype = CALDATE_FIELDS

        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + ["AVG_DURATION", "IUNIT", "NFREQ"]
        )

        # RECEIVER_CODE [Int, 16 bits] = Name of Receiver: 0=TNR; 1=RAD1; 2=RAD2
        # JULIAN_SEC [Int, 32 bits] = Julian date of the middle of the 60-second interval (in seconds since 1950/01/01)

        orbit_fields, orbit_dtype = ORBIT_FIELDS

        header_dtype = _merge_dtype((ccsds_dtype, ">hi", caldate_dtype, ">hhh"))

        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                nfreq = header_i["NFREQ"]

                if self.load_data:
                    # Reading orbit data for current sweep
                    orbit = _read_block(self.file, orbit_dtype, orbit_fields)

                    # Reading frequency list in the current sweep
                    cur_dtype = ">" + "f" * nfreq
                    freq = _read_block(self.file, cur_dtype)

                    # Reading frequency list in the current sweep
                    intensity = _read_block(self.file, cur_dtype)

                    data_i = {
                        "FREQ": freq,
                        "INTENSITY": intensity,
                        "ORBIT": orbit,
                    }
                else:
                    # Skip data section
                    self.file.seek(12 + 8 * nfreq, 1)
                    data_i = None

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

        self._nsweep = nsweep
        return data


class WindWavesRad1L260sV1BinData(
    WindWavesL260sV1BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    pass


class WindWavesRad2L260sV1BinData(
    WindWavesL260sV1BinData, dataset="cdpp_wi_wa_rad2_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v1` binary data"""

    pass


class WindWavesTnrL260sV1BinData(
    WindWavesL260sV1BinData, dataset="cdpp_wi_wa_tnr_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v1` binary data"""

    pass
