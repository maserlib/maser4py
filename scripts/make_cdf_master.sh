#! /bin/bash

#
# PURPOSE:
#   Build skeleton tables and master CDF files from
#   Excel skeleton files in directory.
#
# USAGE:
#   bash make_cdf_master.bash xlsxdir sktdir cdfdir
#
# , where xlsxdir is the directory of the input Excel skeleton files to convert,
# sktdir is the directory where resulting skeleton table files will be saved,
# cdfdir is the directory where resulting CDF master files will be saved.
#
# X.Bonnin, 02-DEC-2015


if [ $# != 3 ]; then
    echo "Usage:"
    echo "bash make_cdf_master.bash xlsxdir sktdir cdfdir"
    exit 0
fi


for excel in `ls $1/*.xlsx`; do
    echo "Running command:"
    basename=$(basename "$excel")
    filename=$(echo $basename | cut -f 1 -d '.')
    skeleton=$2/$filename".skt"
    master=$3/$filename".cdf"

    #echo "Converting "$excel" into "$skeleton
    echo "xlsx2skt -OVIA "$excel" -s "$skeleton
    xlsx2skt -OVIA $excel -s $skeleton

    if [ -e $skeleton ];then
        #echo "Converting "$skeleton" into "$master
        echo "skt2cdf -OV "$skeleton" -c "$output_master
        skt2cdf -OV $skeleton -c $master
    else
        echo "WARNING: "$skeleton" does not exist!"
    fi
done

