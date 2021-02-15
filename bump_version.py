#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to get package version from pyproject.toml file
then write/update a maser/version.py file with __version__ variable inside.
."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import argparse
from pathlib import Path

import toml

# ________________ HEADER _________________________

# # Mandatory
# __version__ = ""
# __author__ = ""
# __date__ = ""
#
# # Optional
# __license__ = ""
# __credit__ = [""]
# __maintainer__ = ""
# __email__ = ""
# __project__ = ""
# __institute__ = ""
# __changes__ = {"X.Y.Z": "modif. history"}


# ________________ Global Variables _____________
# (define here the global variables)

CWD = Path.cwd()

PYPROJECT_PATH = CWD / 'pyproject.toml'
MASER_ROOT_PATH = CWD / 'maser'

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def main():
    """Main program."""

    # Get version from pyproject.toml
    metadata = toml.load(str(PYPROJECT_PATH))
    version = metadata['tool']['poetry']['version']

    # Write __version__ in maser/version.py
    version_file = MASER_ROOT_PATH / 'version.py'
    version_file.write_text('__version__ = "{0}"'.format(version))
    print('{0} file created with __version__ = "{1}"'.format(version_file, version))

    # _________________ Main ____________________________
if __name__ == '__main__':
    # print ""
    main()
