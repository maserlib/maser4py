#! /usr/bin/env bash

# Purpose:
#   Bash script to test the maser.cdf.serializer module
#
# Usage:
#   bash test_cdfconverter.sh
#
# Before running this script, make sure that the maser python package
# is installed on your system (use setup.py to install it), and that
# the directory containing the "skeletoncdf" program
# of the NASA CDF distribution is on your $PATH.
#
# X.Bonnin, 24-NOV-2015

pushd . > /dev/null
workdir="${BASH_SOURCE[0]:-$0}";
while([ -h "${workdir}" ]); do
    cd "`dirname "${workdir}"`"
    workdir="$(readlink "`basename "${workdir}"`")";
done
cd "`dirname "${workdir}"`" > /dev/null
workdir="`pwd`";
popd  > /dev/null

if [[ -z ${CDF_BIN} ]];then
    echo "Warning: it seems that the NASA CDF software environment is not configured correctly!"
    exit -1
fi

inputdir=${workdir}/../maser/support/cdf
outputdir=/tmp

# Input Excel 2007 format file to convert
excel=$inputdir/converter_example.xlsx

echo "Converting Excel file "$excel" into master binary CDF"
maser -D skeletoncdf -I -A -e -o $outputdir $excel


