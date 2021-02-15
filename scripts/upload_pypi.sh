#!/bin/bash

# Publish the package on Pypi (https://pypi.python.org)
# (requires poetry for python: https://python-poetry.org/)
# X.Bonnin, 12-FEB-2021

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

cd $workdir/..

rm -rf dist/

# Create a virtualenv for publishing
venv_dir="/tmp/maser4py_upload_pypi__`date +%Y%m%dT%H%M%s`"
cmd="python3 -m venv $venv_dir"
echo $cmd && eval $cmd
source $venv_dir/bin/activate

# Update pip
cmd="pip install pip -U"
echo $cmd && eval $cmd

# Install poetry
cmd="pip install poetry"
echo $cmd && eval $cmd

# Install package
cmd="poetry install"
echo $cmd && eval $cmd

# Build package
cmd="poetry build"
echo $cmd && eval $cmd

# Upload package in pypi
cmd="poetry publish"
echo $cmd && eval $cmd

# Close virtualenv
deactivate

# Delete virtualenv
echo "Deleting ${venv_dir}"
rm -rf $venv_dir
