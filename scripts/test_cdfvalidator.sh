#! /bin/bash

# Purpose:
#   Script to test the maser.cdf.validator module.
#   This script uses the output cdf of the test_xlsx2skt.sh as input.
#
# Usage:
#   bash test_cdfvalidator.sh
#
# Before running this script, make sure that the maser python package
# is installed on your system (use setup.py to install it), and that
# the directory containing the "skeletoncdf" and "cdfvalidate" programs
# of the NASA CDF distribution is on your $PATH.
#
# X.Bonnin, 24-NOV-2015

pushd `dirname $0` > /dev/null
scriptpath=`pwd`
popd > /dev/null

# CDF format file to validate
cdffile=/tmp/converter_example.cdf

# JSON Validator model example file
jsonfile=$scriptpath/../maser/support/cdf/validator_model_example.json

if [ ! -f $cdffile ]; then
    echo $cdffile" does not exist, and will be created..."
    bash $scriptpath/test_cdfconverter.sh
fi

# Perform all of the validation tests available
cdfvalid -VC $cdffile -m $jsonfile

