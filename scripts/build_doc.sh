#! /usr/bin/env bash

# PURPOSE:
# Bash script to build the MASER-PY documentation.
# Documentation required to use sphinx Python software.
#
# USAGE:
#   bash build_doc.sh [docdir]
#
#, where [docdir] is an optional input argument providing the MASER-PY doc. directory.
# If it is not provided, the script assumed that the docdir is in ../doc from the current directory.
#
# LAST MODIF.:
# X.Bonnin, 07-DEC-2015


if [ $# = 1 ]; then
    docdir=$1
else
    pushd `dirname $0` > /dev/null
    scriptpath=`pwd`
    popd > /dev/null
    docdir=$scriptpath/../doc
fi

currentdir=`pwd`
cd $docdir

# Build doc
sphinx-build source build

# Build api doc
sphinx-apidoc -o build ../maser

# Create pdf version
make latexpdf

cd $currentdir





