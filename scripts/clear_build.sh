#!/bin/bash

# Clear the package build

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

# go to maser4py main dir
cd $workdir/..

if [[ -d "build" ]];then
    echo "Deleting build/..."
    rm -rf build
fi

if [[ -d "dist" ]];then
    echo "Deleting dist/..."
    rm -rf dist
fi

if [[ -d "maser4py.egg-info" ]];then
    echo "Deleting maser4py.egg-info..."
    rm -rf maser4py.egg-info
fi
