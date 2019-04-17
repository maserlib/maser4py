#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python script to modify CDF Excel template files
Required maser4py package https://pypi.org/project/maser4py/.
."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import os
import argparse
from pathlib import Path
import json

from maser.utils.cdf.serializer.xlsx import set_gattr_entries, \
    add_gattr_entry, add_gattr, rm_gattr, set_vattr_entry, \
    rm_vattr, rename_gattr, set_gattr_dtype, rename_zvar, \
    set_zvar_entry, rm_zvar, add_zvar


# ________________ HEADER _________________________

# Mandatory
__version__ = "0.2.0"
__author__ = "X.Bonnin"
__date__ = "2019-03-31" \
           ""

# Optional
__license__ = "MIT"
__credit__ = [""]
__maintainer__ = "X.Bonnin"
__email__ = ""
__project__ = "RPW Operations Centre"
__institute__ = "LESIA"
__changes__ = {"0.1.0": "First release",
               "0.2.0": "Add new change possibilities"}


# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def main():
    """Main program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", nargs=1, type=Path,
                        help="JSON file containing the "
                        "attributes to set")
    parser.add_argument("xlsx_files", type=Path, nargs='+',
                        help="Excel file(s) containing CDF skeleton content.")
    parser.add_argument("-o", "--output-dir", nargs=1, type=Path,
                        default=[None], help="output directory")
    parser.add_argument("-F", "--force-add", action='store_true',
                        help="Force global attribute adding if not "
                        "found when setting is requested "
                        "(use CDF_CHAR dtype by default).")

    args = parser.parse_args()
    outdir = args.output_dir[0]
    overwrite = True

    if not outdir.is_dir():
        os.mkdir(outdir)
        print(f"--> {outdir} output directory created.")

    with open(str(args.json_file[0]), "r") as jfile:
        jdata = json.load(jfile)

    # Loop on input Excel files
    output = None
    for xlsx in args.xlsx_files:

        if outdir is not None:
            output = outdir / xlsx.name

        file = xlsx
        print(f"--> Processing {xlsx}")

        if "add_gattr" in jdata:
            for gatt in jdata["add_gattr"]:
                print(f"> Adding \"{gatt['name']}\" with the entry \"{gatt['entries']}\"")
                add_gattr(str(file), gatt['name'], gatt['cdftype'], gatt['entries'],
                          output=str(output), overwrite=overwrite)
                if output.exists():
                    file = output

        if "add_gattr_entry" in jdata:
            for gatt in jdata["add_gattr_entry"]:
                print(f"> Adding entry \"{gatt['entry']}\" into \"{gatt['name']}\"")
                add_gattr_entry(str(output), gatt['name'], gatt['entry'],
                                output=str(output), overwrite=overwrite)

        if "rename_gattr" in jdata:
            for gatt in jdata["rename_gattr"]:
                print(f"> Renaming \"{gatt['name']}\" into \"{gatt['new_name']}\"")
                rename_gattr(str(output), gatt['name'], gatt['new_name'],
                             output=str(output), overwrite=overwrite)

        if "rm_gattr" in jdata:
            for gatt in jdata["rm_gattr"]:
                print(f"> Removing \"{gatt['name']}\"")
                rm_gattr(str(output), gatt['name'],
                         output=str(output), overwrite=overwrite)

        if "set_gattr_entries" in jdata:
            for gatt in jdata["set_gattr_entries"]:
                print(f"> Setting \"{gatt['name']}\" with entry \"{gatt['entries']}\"")
                is_done = set_gattr_entries(str(output), gatt['name'], gatt['entries'],
                                            output=str(output), overwrite=overwrite)
                if is_done is False and args.force_add:
                    print(f"> Adding \"{gatt['name']}\" with entry \"{gatt['entries']}\"")
                    add_gattr(str(output), gatt['name'], "CDF_CHAR", gatt['entries'],
                              output=str(output), overwrite=overwrite)

        if "set_gattr_dtype" in jdata:
            for gatt in jdata["set_gattr_dtype"]:
                print(f"> Changing \"{gatt['name']}\" dtype into \"{gatt['new_dtype']}\"")
                set_gattr_dtype(str(output), gatt['name'], gatt['new_dtype'],
                                output=str(output), overwrite=overwrite)

        if "add_zvar" in jdata:
            for zvar in jdata["add_zvar"]:
                print(f"> Adding \"{zvar['name']}\" zVariable")
                entry = [zvar["name"],
                         zvar["dtype"],
                         zvar["num"],
                         zvar["dims"],
                         zvar["sizes"],
                         zvar["recvar"],
                         ]
                if int(zvar['dims']) != 0:
                    entry.append(zvar["dimvar"])

                add_zvar(str(output), entry,
                         output=str(output),
                         overwrite=overwrite)

        if "rename_zvar" in jdata:
            for zvar in jdata["rename_zvar"]:
                print(f"> Renaming \"{zvar['name']}\" zVariable into \"{zvar['new_name']}\"")
                rename_zvar(str(output), zvar['name'],
                            zvar['new_name'],
                            output=str(output),
                            overwrite=overwrite)

        # TODO - Set not only dtype
        if "set_zvar_entry" in jdata:
            for zvar in jdata["set_zvar_entry"]:
                if "dtype" in zvar:
                    dtype = zvar["dtype"]
                else:
                    dtype = None
                print(f"> Setting \"{zvar['name']}\" zVariable")
                set_zvar_entry(str(output), zvar['name'],
                               dtype=dtype,
                               output=str(output),
                               overwrite=overwrite)

        if "rm_zvar" in jdata:
            for zvar in jdata["rm_zvar"]:
                print(f"> Removing \"{zvar['name']}\" zVariable")
                rm_zvar(str(output), zvar['name'],
                        output=str(output),
                        overwrite=overwrite)

        if "set_vattr_entries" in jdata:
            for vatt in jdata["set_vattr_entries"]:
                print(f"> Setting \"{vatt['name']}\" with entry \"{vatt['entry']}\" for the variable \"{vatt['varname']}\"")
                set_vattr_entry(str(output), vatt['name'], vatt['entry'],
                                varname=vatt['varname'],
                                output=str(output), overwrite=overwrite)

        if "rm_vattr" in jdata:
            for vatt in jdata["rm_vattr"]:
                print(f"> Removing \"{vatt['name']}\" for the variable \"{vatt['varname']}\"")
                rm_vattr(str(output), vatt['name'],
                         varname=vatt['varname'],
                         output=str(output),
                         overwrite=overwrite)

        print(f"--> Saving into {output}")

    # _________________ Main ____________________________
if __name__ == "__main__":
    # print ""
    main()
