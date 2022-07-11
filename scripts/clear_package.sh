#!/bin/bash

#   Erase a Python package providing the list of
#   files generated during the install
#
# Usage:
#   clear_package file
#
#, where file.txt contains the files generated during the package install.
#
# Note:
#   Use command "python setup.py install --record files.txt" in order
#   to record into a file.txt text file generated package files during install
#
# Modification History:
#   Written by X.Bonnin, 06-APR-2016
#

if [ $# != 1 ]; then
    echo "Usage:"
    echo "clear_package file"
    exit 0
fi

cat $1 | xargs rm -rfv
