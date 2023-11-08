# -*- coding: utf-8 -*-
from ..plot import Pds3DataTablePlot, Pds3DataTimeSeriesPlot
from pathlib import Path
from typing import Union, List

# ===================================================================
# VOYAGER-PRA-3-RDR-LOWBAND-6SEC datasets
# ===================================================================


class VgPra3RdrLowband6secV1Plot(
    Pds3DataTablePlot,
    dataset="VGX-X-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager 1 or 2 PRA Level 3 RDR LowBand
    6sec PDS3 dataset.
    """

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["L", "R"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )


class Vg1JPra3RdrLowband6secV1Plot(
    VgPra3RdrLowband6secV1Plot,
    dataset="VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager-1/PRA Jupiter Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2JPra3RdrLowband6secV1Plot(
    VgPra3RdrLowband6secV1Plot,
    dataset="VG2-J-PRA-3-RDR-LOWBAND-6SEC-V1.0",
):
    """Class for the Voyager-2/PRA Jupiter Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-J-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg1SPra3RdrLowband6secV1Plot(
    VgPra3RdrLowband6secV1Plot, dataset="VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-1/PRA Saturn Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2SPra3RdrLowband6secV1Plot(
    VgPra3RdrLowband6secV1Plot, dataset="VG2-S-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-2/PRA Saturn Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-S-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2NPra3RdrLowband6secV1Plot(
    VgPra3RdrLowband6secV1Plot, dataset="VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-2/PRA Neptune Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


class Vg2UPra3RdrLowband6secV1Plot(
    VgPra3RdrLowband6secV1Plot, dataset="VG2-U-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    """Class for the Voyager-2/PRA Uranus Level 3 RDR LowBand 6sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-U-PRA-3-RDR-LOWBAND-6SEC-V1.0`."""

    pass


# ===================================================================
# VOYAGER-PRA-4-SUMM-BROWSE-48SEC datasets
# ===================================================================


class VgPra4RSummBrowse48secV1Plot(
    Pds3DataTimeSeriesPlot,
    dataset="VGX-X-PRA-4-SUMM-BROWSE-48SEC-V1.0",
):
    """Class for the Voyager 1 or 2 PRA Level 4 Summary Browse
    48sec PDS3 dataset.
    """

    def main_plot(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["L", "R"],
        **kwargs,
    ):
        self._main_plot(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )


class Vg1JPra4SummBrowse48secV1Plot(
    VgPra4RSummBrowse48secV1Plot, dataset="VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-1/PRA Jupiter Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


class Vg2JPra4SummBrowse48secV1Plot(
    VgPra4RSummBrowse48secV1Plot, dataset="VG2-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-2/PRA Jupiter Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-J-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


class Vg2NPra4SummBrowse48secV1Plot(
    VgPra4RSummBrowse48secV1Plot, dataset="VG2-N-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-2/PRA Neptune Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-N-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


class Vg2UPra4SummBrowse48secV1Plot(
    VgPra4RSummBrowse48secV1Plot, dataset="VG2-U-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    """Class for the Voyager-2/PRA Uranus Level 4 Summary Browse
    48sec PDS3 dataset.

    PDS3 DATASET-ID: `VG2-U-PRA-4-SUMM-BROWSE-48SEC-V1.0`."""

    pass


# ===================================================================
# VOYAGER-PRA-2-RDR-HIHRATE-60MS datasets
# ===================================================================


class Vg2NPra2RdrHighrate60msV1Plot(
    Pds3DataTablePlot, dataset="VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1.0"
):
    pass
