#! /usr/bin/env python3
# -*- coding:Utf8 -*-

"""setup.py file for maser4py."""


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
    long_description=open("README.rst").read(),
    author="X.Bonnin",
    license="BSD",
    packages=packages,
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "maser4py=maser.maser:main",
            "xlsx2skt=maser.utils.cdf.converter:xlsxskt",
            "skt2cdf=maser.utils.cdf.converter:sktcdf",
            "cdfvalid=maser.utils.cdf.validator:main",
            "leapsec=maser.utils.cdf.leapsec:main",
            "maser-rpw=maser.data.solo.rpw:main"],
    },
    setup_requires=['numpy>=1.11.0'],
    install_requires=['openpyxl>=2.3.5', 'numpy>=1.11.0'],
    include_package_data=True,
    url="https://github.com/maserlib/maser4py"
    # ext_modules=cythonize("maser/rpl/*.pyx"),
)
