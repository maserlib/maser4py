# -*- coding: utf-8 -*-
from maser.data.base import Records
from ..const import CCSDS_CDS_FIELDS
from ..utils import _merge_dtype, _read_sweep_length
import struct


class WindWavesTnrL3Bqt1mnRecords(Records):
    @property
    def generator(self):
        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS

        header_fields = ccsds_fields + ["UR8_TIME"]

        # UR8_TIME [Real, 64 bits] = Days since 1982/01/01 (=0)

        header_dtype = _merge_dtype((ccsds_dtype, ">d"))
        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                block = self.file.read(16)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))

                if self.load_data:
                    # Reading data from NN in the current sweep
                    block = self.file.read(4)
                    data_from_nn = struct.unpack(">f", block)
                    plasma_freq_nn = data_from_nn[0]

                    # Reading data from Fit in the current sweep
                    block = self.file.read(16)
                    data_from_fit = struct.unpack(">ffff", block)
                    plasma_freq_fit = data_from_fit[0]
                    cold_elec_temp_fit = data_from_fit[1]
                    elec_dens_ratio = data_from_fit[2]
                    elec_temp_ratio = data_from_fit[3]

                    # Reading data from 3dp in the current sweep
                    block = self.file.read(8)
                    data_from_3dp = struct.unpack(">ff", block)
                    proton_temp_3dp = data_from_3dp[0]
                    sw_veloc_3dp = data_from_3dp[1]

                    # Reading fit accuracy in the current sweep
                    block = self.file.read(28)
                    params = struct.unpack(">fffffff", block)
                    accur_param_1 = params[0]
                    accur_param_2 = params[1]
                    accur_param_3 = params[2]
                    accur_param_4 = params[3]
                    accur_param_7 = params[4]
                    accur_param_8 = params[5]
                    accur_rms = params[6]

                    data_i = {
                        "PLASMA_FREQUENCY_NN": plasma_freq_nn,
                        "PLASMA_FREQUENCY": plasma_freq_fit,
                        "COLD_ELECTRONS_TEMPERATURE": cold_elec_temp_fit,
                        "ELECTRONIC_DENSITY_RATIO": elec_dens_ratio,
                        "ELECTRONIC_TEMPERATURE_RATIO": elec_temp_ratio,
                        "PROTON_TEMPERATURE": proton_temp_3dp,
                        "SOLAR_WIND_VELOCITY": sw_veloc_3dp,
                        "FIT_ACCUR_PARAM_1": accur_param_1,
                        "FIT_ACCUR_PARAM_2": accur_param_2,
                        "FIT_ACCUR_PARAM_3": accur_param_3,
                        "FIT_ACCUR_PARAM_4": accur_param_4,
                        "FIT_ACCUR_PARAM_7": accur_param_7,
                        "FIT_ACCUR_PARAM_8": accur_param_8,
                        "FIT_ACCUR_RMS": accur_rms,
                    }
                else:
                    # Skip data section
                    self.file.seek(56, 1)
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
                yield header_i, data_i
                nsweep += 1
