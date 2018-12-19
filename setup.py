#! /usr/bin/env python3
# -*- coding:Utf8 -*-

"""setup.py file for maser4py."""


# --------------------------------------------------------------------------------------------------------------
# All necessary import:
# --------------------------------------------------------------------------------------------------------------
import os.path as osp
import re
import sys

from setuptools import find_packages
from setuptools import setup
from doc.utils import APIDoc

# --------------------------------------------------------------------------------------------------------------
# Global variables:
# --------------------------------------------------------------------------------------------------------------


packages = find_packages()


ROOT_DIRECTORY = osp.dirname(osp.abspath(__file__))
REQ_FILE = osp.join(ROOT_DIRECTORY, "requirements.txt")
CHANGELOG_FILE = osp.join(ROOT_DIRECTORY, "CHANGELOG.rst")


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


def get_version(changelog):
    """Get latest version from the input CHANGELOG.rst file."""
    pattern = re.compile(r"(\d*)\.(\d*)\.(\w*)")
    if osp.isfile(changelog):
        with open(changelog, 'rt') as file:
            for line in file:
                if pattern.match(line):
                    return line.strip()

    print("WARNING: CHANGELOG.rst not found or invalid, version unknown!")
    return "unknown"

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
    version=get_version(CHANGELOG_FILE),
    description="Python 3 module for the MASER portal",
    long_description=open(osp.join(ROOT_DIRECTORY, "README.rst")).read(),
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
