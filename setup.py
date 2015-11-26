#! /usr/bin/env python3
# -*- coding:Utf8 -*-

# --------------------------------------------------------------------------------------------------------------
# All necessary import:
# --------------------------------------------------------------------------------------------------------------
#import versioneer

from setuptools import find_packages
from setuptools import setup
from doc.utils import APIDoc


# for management of the version string from various VCS
# versioneer.VCS = "git"
# versioneer.versionfile_source = "maser/_version.py"
# versioneer.versionfile_build = "maser/_version.py"
# versioneer.tag_prefix = ""
# versioneer.parentdir_prefix = "maser-"

#packages = find_packages(exclude=["rgts.tv", "tests"])

# --------------------------------------------------------------------------------------------------------------
# Call the setup function:
# --------------------------------------------------------------------------------------------------------------

# set the command classes to use
cmdclass = {
    "build_doc": APIDoc,
}
#cmdclass.update(versioneer.get_cmdclass())

setup(
    name='MASER-PY: Mesures, Analyses et Simulations d’Emissions Radio for Python',
    version='0.1.0',
    description="Python 3 module for maser",
    author="X.Bonnin",
#  packages=packages,
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": ["maser=maser:main",
            "xlsx2skt=maser.cdf.xlsx2skt:main",
            "cdfvalidator=maser.cdf.cdfvalidator:main"
            ],
    },
    #ext_modules=cythonize("maser/rpl/*.pyx"),
)
