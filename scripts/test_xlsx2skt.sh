#! /bin/bash

# Bash script to test the maser.cdf.xlsx2skt module
#
# Usage:
#   bash test_xlsx2skt.sh
#
# Before running this script, make sure that the maser python package
# is installed on the system (use setup.py), and the skeletoncdf
# program directory is on the $PATH env. variable.
#
# X.Bonnin, 24-NOV-2015

echo $PATH

currentpath=`pwd`

pushd `dirname $0` > /dev/null
scriptpath=`pwd`
popd > /dev/null

inputdir=$scriptpath/../support/examples
outputdir=$scriptpath/../tmp

input_xlsx=$inputdir/xlsx2skt_example.xlsx
output_skeleton=$outputdir/xlsx2skt_example.skt
output_master=$outputdir/xlsx2skt_example.cdf

xlsx2skt -OVIA $input_xlsx -s $output_skeleton -c $output_master
