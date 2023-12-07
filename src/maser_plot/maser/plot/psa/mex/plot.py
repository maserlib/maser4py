# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union, List
from ...pds import Pds3Plot


class MexMMarsis3RdrAisV1Plot(
    Pds3Plot,
    dataset="MEX-M-MARSIS-3-RDR-AIS-V1.0",
):
    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["SPECTRAL_DENSITY_MED", "SPECTRAL_DENSITY_AVG"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )


class MexMMarsis3RdrAisExt1V1Plot(
    MexMMarsis3RdrAisV1Plot, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT1-V1.0"
):
    pass


class MexMMarsis3RdrAisExt2V1Plot(
    MexMMarsis3RdrAisV1Plot, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT2-V1.0"
):
    pass


class MexMMarsis3RdrAisExt3V1Plot(
    MexMMarsis3RdrAisV1Plot, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT3-V1.0"
):
    pass


class MexMMarsis3RdrAisExt4V1Plot(
    MexMMarsis3RdrAisV1Plot, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT4-V1.0"
):
    pass


class MexMMarsis3RdrAisExt5V1Plot(
    MexMMarsis3RdrAisV1Plot, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT5-V1.0"
):
    pass


class MexMMarsis3RdrAisExt6V1Plot(
    MexMMarsis3RdrAisV1Plot, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT6-V1.0"
):
    pass
