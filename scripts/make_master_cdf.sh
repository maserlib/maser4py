#!/bin/bash

# Make master cdf from CDF template Excel files
# using maser skeletoncdf program
# X.Bonnin, 23/01/2019

if [[ $# < 2 ]];then
    echo "Usage:"
    echo "make_master_cdf.sh outdir input_file [input_file ...]"
    exit 0
fi

outdir=$1
shift
infiles=$@

echo $outdir
echo $infiles

if [ ! -f $outdir ];then
    echo "$outdir folder not found, create it..."
    mkdir -p $outdir
fi

maser skeletoncdf -IAe -o $outdir $infiles
