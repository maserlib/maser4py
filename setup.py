#! /usr/bin/env python3
# -*- coding:Utf8 -*-

# --------------------------------------------------------------------------------------------------------------
# All necessary import:
# --------------------------------------------------------------------------------------------------------------
# import versioneer

from setuptools import find_packages
from setuptools import setup
from doc.utils import APIDoc
from maser import _version


# for management of the version string from various VCS
# versioneer.VCS = "git"
# versioneer.versionfile_source = "maser/_version.py"
# versioneer.versionfile_build = "maser/_version.py"
# versioneer.tag_prefix = ""
# versioneer.parentdir_prefix = "maser-"

packages = find_packages()

# --------------------------------------------------------------------------------------------------------------
# Call the setup function:
# --------------------------------------------------------------------------------------------------------------

# set the command classes to use
cmdclass = {
    "build_doc": APIDoc,
}
# cmdclass.update(versioneer.get_cmdclass())

setup(
    name='maser',
    version=_version.__version__,
    description="Python 3 module for MASER",
    author="X.Bonnin",
    packages=packages,
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "maser=maser.maser:main",
            "maser-py=maser.maser:main",
            "xlsx2skt=maser.utils.cdf.cdfconverter:xlsxskt",
            "skt2cdf=maser.utils.cdf.cdfconverter:sktcdf",
            "cdfvalidator=maser.utils.cdf.cdfvalidator:main"],
    },
    install_requires=['openpyxl', 'simplejson', 'numpy'],
    include_package_data=True
    # ext_modules=cythonize("maser/rpl/*.pyx"),
)
