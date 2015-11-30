#! /bin/bash

# Purpose:
#   Bash script to test the maser.cdf.xlsx2skt module
#
# Usage:
#   bash test_xlsx2skt.sh
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

inputdir=$scriptpath/../support/cdf
outputdir=/tmp

# Input Excel 2007 format file to read
input_xlsx=$inputdir/xlsx2skt_example.xlsx
# Output skeleton table to create
output_skeleton=$outputdir/xlsx2skt_example.skt
# Output master cdf file to create
output_master=$outputdir/xlsx2skt_example.cdf

echo "xlsx2skt -OVIA "$input_xlsx" -s "$output_skeleton" -c "$output_master
xlsx2skt -OVIA $input_xlsx -s $output_skeleton -c $output_master
