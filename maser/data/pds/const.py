from maser.data.pds.cassini.rpws.wbr import PDSPPICassiniRPWSWBRFullResDataFromLabel
from maser.data.pds.cassini.rpws.hfr import PDSPPICassiniRPWSHFRLowRateFullDataFromLabel
from maser.data.pds.voyager.pra import PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel, \
    PDSPPIVoyagerPRAHighRateDataTimeSeriesDataFromLabel

__all__ = ['PDS_OBJECT_CLASSES']

PDS_OBJECT_CLASSES = {
    'CO-V/E/J/S/SS-RPWS-2-REFDR-WBRFULL-V1.0': PDSPPICassiniRPWSWBRFullResDataFromLabel,
    'CO-V/E/J/S/SS-RPWS-3-RDR-LRFULL-V1.0': PDSPPICassiniRPWSHFRLowRateFullDataFromLabel,
    'VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-J-PRA-3-RDR-LOWBAND-6SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-S-PRA-3-RDR-LOWBAND-6SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-U-PRA-3-RDR-LOWBAND-6SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG1-S-PRA-4-SUMM-BROWSE-48SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-J-PRA-4-SUMM-BROWSE-48SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-S-PRA-4-SUMM-BROWSE-48SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-N-PRA-4-SUMM-BROWSE-48SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-U-PRA-4-SUMM-BROWSE-48SEC-V1.0': PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel,
    'VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1.0': PDSPPIVoyagerPRAHighRateDataTimeSeriesDataFromLabel,
}
