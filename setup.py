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
    name='maser4py',
    version=_version.__version__,
    description="Python 3 module for the MASER portal",
    long_description=open("README.rst").read(),
    author="X.Bonnin",
    author_email="xavier.bonnin@obspm.fr",
    license="BSD",
    packages=packages,
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "maser=maser.script:main",
            "xlsx2skt=maser.utils.cdf.converter:xlsxskt",
            "skt2cdf=maser.utils.cdf.converter:sktcdf",
            "cdfvalid=maser.utils.cdf.validator:main",
            "leapsec=maser.utils.time.leapsec:main",
            "maser-rpw=maser.data.solo.rpw:main"],
    },
    install_requires=['openpyxl>=2.3.5', 'numpy>=1.11.0',
                      'matplotlib', 'sphinx>=1.4.1', 'pytz',
                      'sphinx_rtd_theme'],
    include_package_data=True,
    url="https://github.com/maserlib/maser4py"
    # ext_modules=cythonize("maser/rpl/*.pyx"),
)
