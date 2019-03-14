from .rpws.hfr import PDSPPICassiniRPWSHFRLowRateFullDataFromLabel
from .rpws.wbr import PDSPPICassiniRPWSWBRFullResDataFromLabel

__ALL__ = ['PDS_OBJECT_CLASSES']

PDS_OBJECT_CLASSES = {
    'CO-V/E/J/S/SS-RPWS-2-REFDR-WBRFULL-V1.0': PDSPPICassiniRPWSWBRFullResDataFromLabel,
    'CO-V/E/J/S/SS-RPWS-3-RDR-LRFULL-V1.0': PDSPPICassiniRPWSHFRLowRateFullDataFromLabel
}
