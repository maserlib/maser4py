#! /bin/bash

# Purpose:
#   Bash script to test the maser.cdf.cdfconverter module
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

pushd `dirname $0` > /dev/null
scriptpath=`pwd`
popd > /dev/null

inputdir=$scriptpath/../maser/support/cdf
outputdir=/tmp

# Input Excel 2007 format file to convert
excel=$inputdir/cdfconverter_example.xlsx
# Output skeleton table to create
skeleton=$outputdir/cdfconverter_example.skt
# Output master cdf file to create
master=$outputdir/cdfconverter_example.cdf

echo "Converting "$excel" into "$skeleton
echo "xlsx2skt -OVIA "$excel" -s "$skeleton
xlsx2skt -OVIA $excel -s $skeleton

echo "Converting "$skeleton" into "$master
echo "skt2cdf -OV "$skeleton" -c "$output_master
skt2cdf -OV $skeleton -c $master

