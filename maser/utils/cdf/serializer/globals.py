
import os
from maser.settings import SUPPORT_DIR

JINJA_TEMPLATE_DIR = os.path.join(SUPPORT_DIR, "cdf")

SHEETS = {
    "header": [
        "CDF NAME",
        "DATA ENCODING",
        "MAJORITY",
        "FORMAT",
        "CDF_COMPRESSION",
        "CDF_CHECKSUM",
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
        "Dimension Variances",
        "VAR_COMPRESSION",
        "VAR_SPARESERECORDS",
        "VAR_PADVALUE",
    ],
    "VARIABLEattributes": [
        "Variable Name",
        "Attribute Name",
        "Data Type",
        "Value"
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
RVARS = "variables"
NRV = "NRV"
END = "end"

NEW_HEADER = "!VariablesG.AttributesV.AttributesRecordsDimsSizes"
NEW_ZVAR = "!VariableDataNumberRecordDimension"
NEW_VATTRS = "!AttributeData"
NO_NRV = "!RVvalueswerenotrequested."
NEW_NRV = "!NRVvaluesfollow..."