# -*- coding: utf-8 -*-
from maser.data.base import Sweeps
from maser.data.base.sweeps import Sweep
import numpy


class StereoWavesLfrL2HighResSweep(Sweep):
    def __init__(self, header, data):

        sweep_header = dict(zip((11, 12, 13), header))
        sweep_header["nfreq"] = 48
        sweep_header["nconfig"] = max([h["NCONFIG"] for h in header])
        sweep_dtype = [
            ("receiver_code", int),
            ("integ_time", float),
            ("step_time", float),
            ("freq", float),
            ("agc1", float),
            ("agc2", float),
            ("auto1", float),
            ("auto2", float),
            ("crossr", float),
            ("crossi", float),
        ]
        sweep_data = numpy.zeros(
            (sweep_header["nfreq"], sweep_header["nconfig"]), dtype=sweep_dtype
        )

        for sub_sweep_head, sub_sweep_data in zip(header, data):
            irec = (sub_sweep_head["RECEIVER_CODE"] % 10) - 1
            sweep_data[irec * 16 : (irec + 1) * 16]["receiver_code"] = sub_sweep_head[
                "RECEIVER_CODE"
            ]
            sweep_data[irec * 16 : (irec + 1) * 16]["integ_time"] = sub_sweep_head[
                "INTEG_TIME"
            ]
            sweep_data[irec * 16 : (irec + 1) * 16]["freq"] = numpy.array(
                sub_sweep_data["freq"]
            ).reshape(16, sweep_header["nconfig"])
            sweep_data[irec * 16 : (irec + 1) * 16]["step_time"] = sub_sweep_data[
                "step_time"
            ]
            sweep_data[irec * 16 : (irec + 1) * 16]["agc1"] = sub_sweep_data["agc1"]
            sweep_data[irec * 16 : (irec + 1) * 16]["agc2"] = sub_sweep_data["agc2"]
            sweep_data[irec * 16 : (irec + 1) * 16]["auto1"] = sub_sweep_data["auto1"]
            sweep_data[irec * 16 : (irec + 1) * 16]["auto2"] = sub_sweep_data["auto2"]
            sweep_data[irec * 16 : (irec + 1) * 16]["crossr"] = sub_sweep_data.get(
                "crossr", None
            )
            sweep_data[irec * 16 : (irec + 1) * 16]["crossi"] = sub_sweep_data.get(
                "crossi", None
            )
        super(StereoWavesLfrL2HighResSweep, self).__init__(sweep_header, sweep_data)


class StereoWavesLfrL2HighResSweeps(Sweeps):
    @property
    def generator(self):

        for rec in self.data_reference._data:

            # "RECEIVER_CODE" values are successively 11, 12 and 13, and repeating.
            rec_code = rec["hdr"]["RECEIVER_CODE"]

            # init at the first of the 3 elements
            if rec_code == 11:
                sweep_head = []
                sweep_data = []

            # accumulate header and data
            sweep_head.append(rec["hdr"])
            sweep_data.append(rec["dat"])

            # dispatch at the last of the 3 elements
            if rec_code == 13:

                # create a StereoWavesLfrL2HighResSweep object,
                # accumulated from the 3 last sweeps ("RECEIVER_CODE" = 11, 12 and 13)
                s = StereoWavesLfrL2HighResSweep(sweep_head, sweep_data)

                # yield as many elements as in "nconfig"
                for i in range(s.header["nconfig"]):
                    yield Sweep(s.header, s.data[:, i].reshape(s.header["nfreq"]))
