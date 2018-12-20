#!/bin/bash

# Publish the package on Pypi (https://pypi.python.org)
# X.Bonnin, 20-MAR-2017

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

# Create wheel file
python setup.py bdist_wheel

# Register on Pypi
#twine register `ls dist/*.whl`

# Upload
twine upload dist/*