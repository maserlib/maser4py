#! /usr/bin/env bash

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

# get the script directory
pushd . > /dev/null
workdir="${BASH_SOURCE[0]:-$0}";
while([ -h "${workdir}" ]); do
    cd "`dirname "${workdir}"`"
    workdir="$(readlink "`basename "${workdir}"`")";
done
cd "`dirname "${workdir}"`" > /dev/null
workdir="`pwd`";
popd  > /dev/null

if [[ -n ${CDF_BIN} ]];then
    echo "Warning: it seems that the NASA CDF lib. is not configured correctly!"
    exit -1
fi
. ${CDF_BIN}/definitions.B

# CDF format file to validate
cdffile=/tmp/converter_example.cdf

# JSON Validator model example file
jsonfile=${workdir}/../maser/support/cdf/validator_model_example.json

if [ ! -f $cdffile ]; then
    echo $cdffile" does not exist, and will be created..."
    bash ${workdir}/test_cdfconverter.sh
fi

# Perform all of the validation tests available
cdfvalid -VC $cdffile -m $jsonfile
