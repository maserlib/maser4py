#! /usr/bin/env python3
# -*- coding:Utf8 -*-

"""setup.py file for maser4py."""


# --------------------------------------------------------------------------------------------------------------
# All necessary import:
# --------------------------------------------------------------------------------------------------------------
import os.path as osp

from setuptools import find_packages
from setuptools import setup
from doc.utils import APIDoc
from maser import _version

# --------------------------------------------------------------------------------------------------------------
# Global variables:
# --------------------------------------------------------------------------------------------------------------


packages = find_packages()


ROOT_DIRECTORY = osp.dirname(osp.abspath(__file__))
REQ_FILE = osp.join(ROOT_DIRECTORY, "requirements.txt")


# --------------------------------------------------------------------------------------------------------------
# Call the extra functions:
# --------------------------------------------------------------------------------------------------------------

def get_reqs(req_file):
    """Get module dependencies from requirements.txt."""
    if not osp.isfile(req_file):
        raise BaseException("No requirements.txt file found, aborting!")
    else:
        with open(req_file, 'r') as fr:
            requirements = fr.read().splitlines()

    return requirements


# --------------------------------------------------------------------------------------------------------------
# Call the setup function:
# --------------------------------------------------------------------------------------------------------------

# set the command classes to use
cmdclass = {
    "build_doc": APIDoc,
}

setup(
    name='maser4py',
    install_requires=get_reqs(REQ_FILE),
    version=_version.__version__,
    description="Python 3 module for the MASER portal",
    long_description=open("README.rst").read(),
    author="MASER team",
    license="GPL",
    packages=packages,
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "maser=maser.script:main"]
    },
    include_package_data=True,
    url="https://github.com/maserlib/maser4py"
)
