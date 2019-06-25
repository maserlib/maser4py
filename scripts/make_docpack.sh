#!/bin/bash

# Prepare .zip package containg the maser4py HTML documentation ready to
# be uploade on the http://pythonhosted.org/maser4py web site.
# X.Bonnin (LESIA, CNRS)

# get current script directory
pushd . > /dev/null
workdir="${BASH_SOURCE[0]:-$0}";
while([ -h "${workdir}" ]); do
    cd "`dirname "${workdir}"`"
    workdir="$(readlink "`basename "${workdir}"`")";
done
cd "`dirname "${workdir}"`" > /dev/null
workdir="`pwd`";
popd  > /dev/null

# go to maser4py docs build dir
cd $workdir/../doc/build

# make zip package file
pack=maser4py_docpack.zip
zip -r $pack *

if [[ -f $pack ]];then
    echo "$pack saved"
else
    echo "ERROR: $pack not saved correctly!"
fi

exit 0