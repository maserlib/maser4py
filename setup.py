# -*- coding: utf-8 -*-

# we have to keep a (light version of the) setup.py because
# pyproject.toml is not supporting editable installs via pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version():
    with open("pyproject.toml") as pyproject:
        for line in pyproject.readlines():
            if line.startswith("version"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1] + ".dev"
        else:
            raise RuntimeError("Unable to find version string.")


setup(
    name="maser.data",
    version=get_version(),
    packages=["maser.data"],
    package_dir={"": "."},
    package_data={},
)
