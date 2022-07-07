# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "maser",
    "maser.data",
    "maser.data.base",
    "maser.data.cdpp",
    "maser.data.cdpp.interball",
    "maser.data.cdpp.viking",
    "maser.data.cdpp.wind",
    "maser.data.ecallisto",
    "maser.data.nancay",
    "maser.data.nancay.nda",
    "maser.data.nancay.nenufar",
    "maser.data.pds",
    "maser.data.pds.co",
    "maser.data.pds.vg",
    "maser.data.psa",
    "maser.data.psa.labels",
    "maser.data.psa.mex",
    "maser.data.rpw",
]

package_data = {
    "": ["*"],
    "maser.data": ["psa/labels/MEX-M-MARSIS-3-RDR-AIS-EXT4-V1.0/*"],
}

install_requires = ["astropy>=5.0.4,<6.0.0", "xarray>=2022.3.0,<2023.0.0"]

extras_require = {
    "all": ["nenupy>=2.1.0,<3.0.0", "jupyter>=1.0.0,<2.0.0", "jupytext>=1.13.8,<2.0.0"],
    "jupyter": ["jupyter>=1.0.0,<2.0.0", "jupytext>=1.13.8,<2.0.0"],
    "nenupy": ["nenupy>=2.1.0,<3.0.0"],
    "spacepy": ["spacepy>=0.3.0,<0.4.0"],
}

setup_kwargs = {
    "name": "maser.data",
    "version": "0.1.0",
    "description": "",
    "long_description": None,
    "author": "Baptiste Cecconi",
    "author_email": "baptiste.cecconi@obspm.fr",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "extras_require": extras_require,
    "python_requires": ">=3.8,<4",
}


setup(**setup_kwargs)
