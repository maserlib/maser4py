
import os
from maser.settings import SUPPORT_DIR

JINJA_TEMPLATE_DIR = os.path.join(SUPPORT_DIR, "cdf")

SHEETS = {
    "header": [
        "CDF NAME",
        "DATA ENCODING",
        "MAJORITY",
        "FORMAT"
    ],
    "GLOBALattributes": [
        "Attribute Name",
        "Entry Number",
        "Data Type",
        "Value"
    ],
    "zVariables": [
        "Variable Name",
        "Data Type",
        "Number Elements",
        "Dims",
        "Sizes",
        "Record Variance",
        "Dimension Variances"
    ],
    "VARIABLEattributes": [
        "Variable Name",
        "Attribute Name",
        "Data Type",
        "Value"
    ],
    "Options": [
        "CDF_COMPRESSION",
        "CDF_CHECKSUM",
        "VAR_COMPRESSION",
        "VAR_SPARESERECORDS",
        "VAR_PADVALUE"
    ],
    "NRV": [
        "Variable Name",
        "Index",
        "Value"
    ]
}

HEADER = "header"
GATTRS = "GLOBALattributes"
VATTRS = "VARIABLEattributes"
ZVARS = "zVariables"
OPTS = "Options"
NRV = "NRV"