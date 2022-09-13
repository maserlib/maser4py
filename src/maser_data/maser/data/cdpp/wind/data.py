# -*- coding: utf-8 -*-
from typing import Union
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
import numpy


class WindWavesRad1L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v2"):
    """CDPP Wind Waves RAD1 Level 2 60s-Average (version 2) dataset

    - Observatory/Facility: WIND
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_wi_wa_rad1_l2_60s_v2`
    - Data format: Binary"""

    _iter_sweep_class = WindWavesL260sSweeps


class WindWavesL2BinData(VariableFrequencies, BinData, dataset="cdpp_wi_wa___l2"):
    """Placeholder class for `cdpp_wi_wa_XXX_l2` binary data."""

    _iter_sweep_class = WindWavesL2HighResSweeps

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
        self.fields = ["VSPAL", "VZPAL", "TSPAL", "TZPAL"]
        self.units = ["V2/Hz", "V2/Hz", "V2/Hz", "V2/Hz"]

    def _read_data_block(self, nbytes):
        import struct

        block = self.file.read(nbytes)
        Vspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        block = self.file.read(nbytes)
        Tspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        return Vspal, Tspal

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
                freq = _read_block(self.file, cur_dtype)

                if self.load_data:
                    # Reading intensity and time values for S/SP in the current sweep
                    Vspal, Tspal = self._read_data_block(4 * npalf * nspal)
                    # Reading intensity and time values for Z in the current sweep
                    Vzpal, Tzpal = self._read_data_block(4 * npalf * nzpal)
                    data_i = {
                        "FREQ": freq,
                        "VSPAL": Vspal,
                        "VZPAL": Vzpal,
                        "TSPAL": Tspal,
                        "TZPAL": Tzpal,
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
                data.append((header_i, data_i))
                nsweep += 1

        self._nsweep = nsweep
        return data

    @property
    def times(self):
        if self._times is None:
            times = []
            for header, _ in self.sweeps:
                times.append(
                    Time(
                        f"{header['CALEND_DATE_YEAR']}-{header['CALEND_DATE_MONTH']}-"
                        f"{header['CALEND_DATE_DAY']} {header['CALEND_DATE_HOUR']}:"
                        f"{header['CALEND_DATE_MINUTE']}:{header['CALEND_DATE_SECOND']}"
                    )
                )
            self._times = Time(times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies = []
            for _, data in self.sweeps:
                self._frequencies.append(data["FREQ"] * Unit("kHz"))
        return self._frequencies

    @property
    def _max_sweep_length(self):
        if self.__max_sweep_length is None:
            self.__max_sweep_length = numpy.max([len(f) for f in self.frequencies])
        return self.__max_sweep_length


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
        nsweep = 0

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
                data.append((header_i, data_i))
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
