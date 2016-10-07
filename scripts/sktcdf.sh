#!/usr/bin/env bash

#
# PURPOSE:
#   Build master CDF files from skeleton table
#   file(s) in a given directory.
#
# USAGE:
#   bash make_cdf_master.bash sktpath cdfdir
#
# IMPORTANT:
#   The NASA CDF dist. environment shall be sets.
#
# , where sktpath is the directory, a file or a file pattern (i.e., *.skt) of the input skeleton file(s)
# cdfdir is the directory where resulting CDF master file(s) will be saved.
#
# X.Bonnin, 02-OCT-2016

if [ $# != 2 ]; then
    echo "Usage:"
    echo "sktcdf.sh sktpath cdfdir"
    exit 0
fi

if [[ -d $1 ]];then
    sktpath=$1/*.skt
else
    sktpath=$1
fi

if [[ -n $CDF_BIN ]];then
    . $CDF_BIN/definitions.B
else
    echo "NASA CDF dist. environment is not loaded!"
    exit 1
fi

for skt in `ls $sktpath`; do
    basename=$(basename "$skt")
    filename=$(echo $basename | cut -f 1 -d '.')
    master=$2/$filename".cdf"


    $CDF_BIN/skeletoncdf $skt $master

done