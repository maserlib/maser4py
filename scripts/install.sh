#!/bin/bash

# Install maser4py (requires poetry for python: https://python-poetry.org/)

# get this script directory
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

# Install with poetry
poetry install
