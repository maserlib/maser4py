#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for Python 3 to convert an Excel (.xlsx) file
into a CDF skeleton table (.skt).
"""

# ________________ HEADER _________________________

# Mandatory
__version__ = "1.0.2"
__author__ = "Xavier Bonnin"
__date__ = "30-NOV-2015"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = "Xavier Bonnin"
__email__ = "xavier.bonnin@obspm.fr"
__institute__ = "LESIA, Observatoire de Paris, CNRS"
__project__ = "MASER"
__change__ = {'1.0.0': 'First release',
                            '1.0.1': 'skt_file becomes optional.'
                            ' Fix an error in skeletoncdf calling',
                            '1.0.2': 'xlsx2skt is now a '
                            'module of  the maser package.'
                            'Xlsx2skt class renamed to Convert'}

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import argparse
from datetime import datetime
import subprocess
import logging

from openpyxl import load_workbook
from collections import OrderedDict

from ...tools import which, setup_logging

# ________________ HEADER _________________________

# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

CURRENT_DATETIME = datetime.now()
ROW_LENGTH_MAX = 79
DEF_INDENT = " " * 16

SHEET_NAMES = ["header", "GLOBALattributes",
               "zVariables", "VARIABLEattributes", "Options", "NRV"]

CDF_OPTION_NAMES = ["CDF_COMPRESSION", "CDF_CHECKSUM"]
VAR_OPTION_NAMES = ["VAR_COMPRESSION",
                    "VAR_SPARSERECORDS",
                    "VAR_PADVALUE"]

HEADER_BOARD = "! Variables     G.Attributes     " + \
    "V.Attributes     Records     Dims     Sizes\n"
HEADER_BOARD += "! ---------           ------------     " + \
    "      ------------          -------           ----          -----"
HEADER_SPACE = DEF_INDENT

GLOBAL_BOARD = "! Attribute    Entry        Data\n"
GLOBAL_BOARD += "! Name        Number   Type   Value\n"
GLOBAL_BOARD += "! ---------       ------           ----       -----"

VARIABLE_BOAD = "! Variable      Data      Number " + \
    "                                Record        Dimension\n"
VARIABLE_BOAD += "! Name          Type      Elements" + \
    "   Dims    Sizes    Variance     Variances\n"
VARIABLE_BOAD += "! --------           ----          --------   " + \
    "       ----        -----        --------           ---------"

VATTRS_BOARD = "  ! Attribute    Data\n"
VATTRS_BOARD += "  ! Name        Type   Value\n"
VATTRS_BOARD += "  ! --------         ----       -----"


# ________________ Class Definition __________
# (If required, define here classes)
class Convert:

    """ Class to convert a formatted Excel file into a CDF skeleton table"""

    def __init__(self, xlsx_file,
                 skt_file=None,
                 cdf_file=None,
                 output_dir=None,
                 overwrite=False,
                 ignore_none=False,
                 auto_pad=False,
                 verbose=True,
                 debug=False):

        self.xlsx_file = xlsx_file
        self.overwrite = overwrite
        self.ignore = ignore_none
        self.auto_pad = auto_pad

        self.cdf_items = {}

        if skt_file is None:
            skt_file = os.path.splitext(self.xlsx_file)[0] + ".skt"

        if cdf_file is None:
            cdf_file = os.path.splitext(self.xlsx_file)[0] + ".cdf"

        if output_dir is None:
            output_dir = os.path.basename(xlsx_file)
        else:
            skt_file = os.path.join(output_dir, os.path.basename(skt_file))
            cdf_file = os.path.join(output_dir, os.path.basename(cdf_file))

        self.skt_file = skt_file
        self.cdf_file = cdf_file

    # Setup the logging
        setup_logging(
            filename=None, quiet=False,
            verbose=verbose,
            debug=debug)

    def parse_xlsx(self):

        """Parse the Excel 2007 format file"""

        xlsx = self.xlsx_file

        if not os.path.isfile(xlsx):
            logger.error("Cannot find Excel file called %s!", xlsx)
            raise

        if os.path.splitext(xlsx)[1] != ".xlsx":
            logger.error("Invalid input Excel format!")
            raise

        logger.info("Parsing %s file...", xlsx)
        wkbk = load_workbook(xlsx, read_only=True)
        sheet_names = wkbk.get_sheet_names()

        if ("rVariables" in sheet_names) or ("variables" in sheet_names):
            logger.warning("rVariable type is not supported!")

        sheets = dict()
        for shtn in SHEET_NAMES:
            logger.info("Loading %s sheet...", shtn)
            if shtn not in sheet_names:
                logger.error("Missing %s sheet in the input Excel file!", shtn)
                raise
            else:
                wksht = wkbk[shtn]

                sheet_data = OrderedDict()
                for i, row in enumerate(wksht.rows):
                    cells_i = []
                    for cell in row:
                        if i == 0:
                            sheet_data[cell.value] = []
                        else:
                            cells_i.append(cell.value)
                    if i != 0:
                        for k, key in enumerate(sheet_data):
                            sheet_data[key].append(cells_i[k])

                sheets[shtn] = sheet_data

        self.cdf_items["GLOBALattributes"] = \
            uniq(sheets["GLOBALattributes"]["Attribute Name"],
                 not_none=True)
        self.cdf_items["VARIABLEattributes"] = \
            uniq(sheets["VARIABLEattributes"]["Attribute Name"],
                 not_none=True)
        self.cdf_items["zVariables"] = \
            uniq(sheets["zVariables"]["Variable Name"],
                 not_none=True)
        logger.info("%i GLOBAL attributes returned",
                  len(self.cdf_items["GLOBALattributes"]))
        logger.info("%i Variable attributes returned",
                  len(self.cdf_items["VARIABLEattributes"]))
        logger.info("%i zVariables returned",
                  len(self.cdf_items["zVariables"]))

        return sheets

    def build_skt(self, xlsx_sheets):

        """Build the CDF skeleton table content using the Excel data"""

        logger.info("Building CDF skeleton table body... ")

        skt_name = os.path.splitext(os.path.basename(self.skt_file))[0]
        xlsx_name = os.path.basename(self.xlsx_file)

        file_header = "!Skeleton table for the \"" + skt_name + "\" CDF.\n"
        file_header += "!Generated: " + \
            CURRENT_DATETIME.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        file_header += "!Skeleton table created by xlsx2skt.py V" + \
            __version__ + "\n"
        file_header += "!Skeleton table created from " + xlsx_name + "\n"

        skt_header = self.build_header(xlsx_sheets["header"],
                                       xlsx_sheets["Options"])
        skt_global = self.build_global(xlsx_sheets["GLOBALattributes"])
        skt_vattrs = self.build_vattributes()
        skt_zvars = self.build_zvariables(xlsx_sheets["zVariables"],
                                          xlsx_sheets["VARIABLEattributes"],
                                          xlsx_sheets["Options"],
                                          xlsx_sheets["NRV"],
                                          ignore_none=self.ignore,
                                          auto_pad=self.auto_pad)

        skt_body = "\n".join([file_header, "", skt_header, "",
                              skt_global, "", skt_vattrs, "",
                              skt_zvars, "", "#end"])

        return skt_body

    def write_skt(self, skt_body):

        """Write the CDF skeleton table file"""

        skt = self.skt_file

        if os.path.splitext(skt)[1] != ".skt":
            logger.info(
                ".skt extension will be automatically appended to %s",
                skt)
            skt = skt + ".skt"

        if not (self.overwrite) and (os.path.isfile(skt)):
            logger.warning("%s already exits!", skt)
            return skt

        logger.info("Writing %s...", skt)

        with open(skt, "w") as filew:
            filew.write(skt_body)

        if os.path.isfile(skt):
            return skt
        else:
            return None

    def run(self):

        """Run the complete xlsx to skt conversion process"""

        xlsx_sheets = self.parse_xlsx()
        skt_body = self.build_skt(xlsx_sheets)
        skt_path = self.write_skt(skt_body)

        if skt_path:
            print("%s has been saved" % skt_path)
            return True
        else:
            return False

    def build_header(self, header_sheet, options_sheet):

        """Build the CDF skeleton table header part"""

        logger.info("Building skeleton table header...")

        header_body = ["#header", ""]

        for key, val in header_sheet.items():
            header_body.append(HEADER_SPACE + key + ": " + val[0])

        header_body.append("")
        header_body.append(HEADER_BOARD)

        nglobal = len(self.cdf_items["GLOBALattributes"])
        nvattr = len(self.cdf_items["VARIABLEattributes"])
        nvar = len(self.cdf_items["zVariables"])

        header_board_info = ["    0/" + str(nvar),
                             str(nglobal), str(nvattr), "0/z", "0"]
        header_board_info = "            ".join(header_board_info)
        header_body.append(header_board_info)

        header_opt_info = "\n"
        for opt in CDF_OPTION_NAMES:
            if opt in options_sheet:
                header_opt_info += "!" + opt + ": " + \
                    options_sheet[opt][0] + "\n"
        header_body.append(header_opt_info)

        header_body = "\n".join(header_body)

        logger.info(header_body)

        return header_body

    def build_global(self, global_sheet):

        """Build the CDF skeleton table GLOBALattributes part"""

        logger.info("Building skeleton table global attributes section..")

        global_body = ["#GLOBALattributes", ""]

        global_body.append(GLOBAL_BOARD)

        if global_sheet["Attribute Name"][0] is None:
            logger.error("First Global attribute name must not be null!")
            raise
        else:
            last_valid_attr = global_sheet["Attribute Name"][0]

        nindent = DEF_INDENT
        new_entry = ""
        for i, attr in enumerate(global_sheet["Attribute Name"]):

            if attr is None:
                continue

            if last_valid_attr != attr:
                new_entry += " .\n"
            global_body.append(new_entry)

            enum_i = str(global_sheet["Entry Number"][i])
            dtype_i = str(global_sheet["Data Type"][i])
            value_i = quote(str(global_sheet["Value"][i]), unquote=True)

            if (value_i.lower() == "None") or (value_i == ""):
                value_i = " "

            if int(enum_i) == 1:
                new_entry = "  " + quote(attr) + "        "
            else:
                new_entry = " " * (nindent + 8)

            new_entry += enum_i + ":  " + dtype_i + "    { "

            value_i = truncate_str(value_i,
                                   int(ROW_LENGTH_MAX / 3),
                                   gap=(" " * (len(new_entry) + 12)),
                                   min_length=6)

            new_entry += quote(value_i) + " }"

            if len(new_entry) > ROW_LENGTH_MAX and int(enum_i) == 1:
                nindent = len(attr)
                new_entry = insert_char(new_entry, "\n" + " " * nindent,
                                        nindent + 4)
            elif int(enum_i) == 1:
                nindent = len(attr) + 14

            last_valid_attr = attr

        new_entry += " .\n"
        global_body.append(new_entry)
        global_body = "\n".join(global_body)

        logger.info(global_body)

        return global_body

    def build_vattributes(self):

        """Build the list of variable attributes"""

        logger.info("Building skeleton table variable attributes section...")

        vattrs_body = ["#VARIABLEattributes", ""]

        for vattr in self.cdf_items["VARIABLEattributes"]:
            vattrs_body.append("  " + quote(vattr))

        vattrs_body = "\n".join(vattrs_body)

        logger.info(vattrs_body)

        return vattrs_body

    def build_zvariables(self, zvars_sheet, vattrs_sheet,
                         options_sheet, nrv_sheet,
                         ignore_none=False,
                         auto_pad=True):

        """Build the CDF skeleton table VARIABLEattributes
        and zVariables parts"""

        logger.info("Building skeleton table zvariable section...")

        zvar_body = ["#variables", ""]
        zvar_body.extend(["!No rVariables.", ""])
        zvar_body.extend(["#zVariables", ""])

        for i, zvar in enumerate(zvars_sheet["Variable Name"]):

            if zvar is None:
                if ignore_none:
                    logger.warning("Current zVariable is NoneType, skipping!")
                    continue
                else:
                    logger.error("ERROR: Current zVariable is NoneType!")
                    raise

            zvar_body.append(VARIABLE_BOAD)

            # New zVariable entry
            zvar_body.append("")

            dtype_i = str(zvars_sheet["Data Type"][i])
            nelem_i = str(zvars_sheet["Number Elements"][i])
            dims_i = str(zvars_sheet["Dims"][i])
            sizes_i = str(zvars_sheet["Sizes"][i])
            recvar_i = str(zvars_sheet["Record Variance"][i])
            dimvars_i = str(zvars_sheet["Dimension Variances"][i])

            logger.info("  " + quote(zvar) + "    " + dtype_i +
                      "     " + nelem_i + "     " + dims_i + "     " +
                      sizes_i + "     " + recvar_i + "     " + dimvars_i)

            if dtype_i == "None":
                sys.exit("ERROR: Wrong Data Type for %s!" % (zvar))
            if nelem_i == "None":
                sys.exit("ERROR: Wrong Number Elements for %s!" % (zvar))
            if dims_i == "None":
                sys.exit("ERROR: Wrong Dims for %s!" % (zvar))

            if sizes_i == "None":
                sizes_i = ""
            if dimvars_i == "None":
                dimvars_i = ""

            zvar_entry = "  " + quote(zvar) + "    " + dtype_i + \
                "     " + nelem_i + "     " + dims_i + "     " + \
                sizes_i + "     " + recvar_i + "     " + dimvars_i

            if len(zvar_entry) > ROW_LENGTH_MAX:
                zvar_entry = insert_char(zvar_entry, "\n", len(zvar) + 2)

            zvar_body.append(zvar_entry)

            var_opt_info = "\n"
            for opt in VAR_OPTION_NAMES:
                if opt in options_sheet:
                    if opt == "VAR_PADVALUE" and auto_pad:
                        options_sheet[opt][0] = assign_pad(dtype_i)
                    var_opt_info += "! " + opt + ": " + \
                        options_sheet[opt][0] + "\n"
            zvar_body.append(var_opt_info)

            # Add variable attributes info
            zvar_body.append(VATTRS_BOARD)

            vattr_entry = ""
            for j, vattr_var in enumerate(vattrs_sheet["Variable Name"]):

                if vattr_var == zvar:
                    vattr_entry += "\n"
                    vattr_name = quote(str(vattrs_sheet["Attribute Name"][j]))
                    vattr_dtype = str(vattrs_sheet["Data Type"][j])
                    if vattr_dtype == "None":
                        logger.error("Wrong Data Type for the " +
                                    "attribute %s " +
                                    "of the variable %s !", vattr_name, zvar)
                        raise

                    vattr_value = str(vattrs_sheet["Value"][j])

                    vattr_entry_j = "   " + vattr_name + "    " \
                        + vattr_dtype + "     { "

                    if vattr_dtype == "CDF_CHAR":
                        gap = " " * (2 * len(vattr_entry_j) - 1)
                        vattr_value = truncate_str(vattr_value,
                                                   int(ROW_LENGTH_MAX / 3),
                                                   gap=gap,
                                                   min_length=6)
                        vattr_value = quote(vattr_value)

                    vattr_entry += vattr_entry_j + vattr_value + " }"

            vattr_entry += " .\n"
            zvar_body.append(vattr_entry)

            # Add NRV
            nrv_body = ""
            for k, nrv_k in enumerate(nrv_sheet["Variable Name"]):
                if zvar == nrv_k:
                    idx_k = str(nrv_sheet["Index"][k])
                    val_k = str(nrv_sheet["Value"][k])
                    if (idx_k == "") or (idx_k == "None"):
                        logger.error("Wrong NRV index for %s!", nrv_k)
                        raise
                    nrv_body += "    [" + idx_k + "] = { " + \
                        quote(val_k) + " }\n"

            if len(nrv_body) == 0:
                nrv_body = "  ! RV values were not requested.\n"
            else:
                nrv_body = "  ! NRV values follow...\n\n" + nrv_body

            zvar_body.append(nrv_body)

        zvar_body = "\n".join(zvar_body)
        return zvar_body

    def write_cdf(self, program=None):

        """ Make a CDF Master binary file from a ASCII
        skeleton table using the skeletoncdf program """

        logger.info(os.environ["SHELL"])
        sys.exit(0)

        # If skeletoncdf program path is not provided
        # then search it on the $PATH
        if program is None:
            program = which('skeletoncdf')

        cmd = [program, self.skt_file, "-cdf", self.cdf_file]

        logger.info(" ".join(cmd))
        try:
            res = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output, errors = res.communicate()
        except OSError as e:
            logger.error(e.strerror)
        except subprocess.TimeoutExpired as e:
            logger.error("Time out expired:  %i sec.", e.timeout)
        else:
            if res.wait() == 0:
                return True
            else:
                logger.error("Error running command %s:\n " +
                             "stdout:\n %s \n stderr:\n %s",
                      ' '.join(cmd), str(output), str(errors))

        return False


# ________________ Global Functions __________
def uniq(seq, not_none=False):

    """Get list of unique elements from an input sequence of list type"""

    seen = set()
    seen_add = seen.add
    if not_none:
        return [x for x in seq if not (x in seen or seen_add(x) or x is None)]
    else:
        return [x for x in seq if not (x in seen or seen_add(x))]


def quote(string, unquote=False):

    """Double quote a given string"""

    if string is not None:
        if string.startswith("\""):
            string = string[1:]
        if string.endswith("\""):
            string = string[:-1]
        if unquote:
            return string
        return "\"" + string + "\""


def truncate_str(string, max_length,
                 gap=DEF_INDENT,
                 min_length=3):

    """ truncate a too long CDF_CHAR value"""

    nstr = len(string)
    new_string = ""
    for i, val_c in enumerate(string):
        if i > nstr - min_length:
            new_string += string[i:]
            break
        new_string += val_c
        if (i % max_length == 0) and (i != 0):
            new_string += "\" - \n" + gap + "\""

    return new_string


def insert_char(string, char, pos):

    """ Insert substring in a string """

    return string[:pos] + char + string[pos:]


def assign_pad(data_type):

    """
    Automatically assigns VAR_PADVALUE
    depending to the input data_type
    """
    dtype = data_type.upper()

    if "EPOCH" in dtype:
        return "01-Jan-0000 00:00:00.000"
    elif "TT2000" in dtype:
        return "0000-01-01T00:00:00.000000000"
    elif ("INT" in dtype) or ("BYTE" in dtype):
        return "0"
    elif ("FLOAT" in dtype) or ("REAL" in dtype):
        return "0.0"
    elif "CHAR" in dtype:
        return "\" \""
    else:
        return "None"


def main():

    """xlsx2skt main program"""

    parser = argparse.ArgumentParser(
        description='Convert a Excel 2007 ' +
        'format file into a CDF skeleton table',
        add_help=True)
    parser.add_argument('xlsx_file', nargs='?',
                        default=None,
                        help='Excel 2007 format file (.xlsx)')
    parser.add_argument('-s', '--skt_file', nargs='?',
                        default=None,
                        help='Output CDF skeleton table (.skt)')
    parser.add_argument('-c', '--cdf_file', nargs='?',
                        default=None,
                        help='Output CDF master file (.cdf)')
    parser.add_argument('-e', '--skeletoncdf_exe', nargs='?',
                        default=None,
                        help='Path of the skeletoncdf program executable')
    parser.add_argument('-o', '--output_dir', nargs='?',
                        default=None,
                        help='Path of the output directory')
    parser.add_argument('-O', '--Overwrite', action='store_true',
                        help='Overwrite existing output files')
    parser.add_argument('-V', '--Verbose', action='store_true',
                        help='Verbose mode')
    parser.add_argument('-D', '--Debug', action='store_true',
                        help='Debug mode')
    parser.add_argument('-I', '--Ignore_none', action='store_true',
                        help='Ignore NoneType zVariables')
    parser.add_argument('-A', '--Auto_pad', action='store_true',
                        help='Value of !VAR_PADVALUE ' +
                        'is automatically assigned')
    parser.add_argument('--version', action='store_true',
                        help='Show version')
    parser.add_argument('--change', action='store_true',
                        help='Show change')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    if args.change:
        print(__change__)
        sys.exit(0)

    if not args.xlsx_file:
        parser.print_help()
        sys.exit(0)

    x2s = Convert(**args.__dict__)
    if not x2s.run():
        sys.exit("Error encountered during execution!")

    if args.skeletoncdf_exe or args.cdf_file:
        x2s.write_cdf(program=args.skeletoncdf_exe)

# _________________ Main ____________________________
if __name__ == "__main__":
    main()
