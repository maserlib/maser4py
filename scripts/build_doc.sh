#! /usr/bin/env bash

# PURPOSE:
# Bash script to build the MASER-PY documentation.
# Documentation required to use sphinx Python software.
#
# USAGE:
#   bash build_doc.sh [docdir]
#
#, where [docdir] is an optional input argument providing the MASER-PY docs. directory.
# If it is not provided, the script assumed that the docdir is in ../docs from the current directory.
#
# LAST MODIF.:
# X.Bonnin, 07-DEC-2015


pushd . > /dev/null
workdir="${BASH_SOURCE[0]:-$0}";
while([ -h "${workdir}" ]); do
    cd "`dirname "${workdir}"`"
    workdir="$(readlink "`basename "${workdir}"`")";
done
cd "`dirname "${workdir}"`" > /dev/null
workdir="`pwd`";
popd  > /dev/null

docdir=${1:-$workdir/../docs}

# Create a virtualenv for publishing
venv_dir="/tmp/maser4py_build_doc__`date +%Y%m%dT%H%M%s`"
cmd="python3 -m venv $venv_dir"
echo $cmd && eval $cmd
source $venv_dir/bin/activate

cd $docdir

# Update pip
cmd="pip install pip -U"
echo $cmd && eval $cmd

# Install poetry
cmd="pip install -r requirements.txt"
echo $cmd && eval $cmd

# Build docs
#cmd="sphinx-build -c $docdir src build"
#echo $cmd && eval $cmd

# Build api docs
cmd="sphinx-apidoc -o build/apidoc ../maser"
echo $cmd && eval $cmd

# Create html & pdf version
cmd="sphinx-build -c $docdir -b html src build/latex"
echo $cmd && eval $cmd
cmd="sphinx-build -c $docdir -b latex src build/latex"
echo $cmd && eval $cmd

cmd="cd $docdir/build/latex && make"
echo $cmd && eval $cmd

cd $currentdir

# Close virtualenv
deactivate

# Delete virtualenv
echo "Deleting ${venv_dir}"
rm -rf $venv_dir
