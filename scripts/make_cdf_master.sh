#! /bin/bash

#
# PURPOSE:
#   Build skeleton tables and master CDF files from
#   Excel skeleton files in directory.
#
# USAGE:
#   bash make_cdf_master.bash xlsxdir sktdir cdfdir
#
# , where xlsxpath is the directory, a file or a file pattern (i.e., *.xlsx) of the input Excel
# skeleton file(s) to convert,
# sktdir is the directory where resulting skeleton table file(s) will be saved,
# cdfdir is the directory where resulting CDF master file(s) will be saved.
#
# X.Bonnin, 02-DEC-2015


if [ $# != 3 ]; then
    echo "Usage:"
    echo "bash make_cdf_master.bash xlsxpath sktdir cdfdir"
    exit 0
fi

if [[ -d $1 ]];then
    xlsxpath=$1/*.xlsx
else
    xlsxpath=$1
fi

for excel in `ls $xlsxpath`; do
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

