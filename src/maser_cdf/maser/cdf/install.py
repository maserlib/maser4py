#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to install a given CDF software release.
@Sonny Lion (LESIA)
"""

import argparse
import os
import platform
import subprocess
import tarfile
from io import BytesIO

import requests

DEFAULT_CDF_URL = "http://cdaweb.gsfc.nasa.gov/pub/software/cdf/dist/cdf{cdf_version}/linux/cdf{cdf_version}-dist-cdf.tar.gz"


def get_cdf(raw_cdf_version, install_dir, cdf_url=DEFAULT_CDF_URL):
    # reformat the cdf version from X.Y.Z to XY_Z
    X, Y, Z = raw_cdf_version.split(".")
    cdf_version = f"{X}{Y}_{Z}"

    # build the url with the cdf version
    url = cdf_url.format(cdf_version=cdf_version)

    response = requests.get(url)
    with tarfile.open(fileobj=BytesIO(response.content), mode="r:gz") as tar:
        tar.extractall(path=install_dir)


def make_cdf(raw_cdf_version, install_dir):
    # reformat the cdf version from X.Y.Z to XY_Z
    X, Y, Z = raw_cdf_version.split(".")
    cdf_version = f"{X}{Y}_{Z}"

    # prepare the make command
    command = ["make", "-C", os.path.join(install_dir, f"cdf{cdf_version}-dist")]
    if platform.system() == "Linux":
        command += ["OS=linux", "ENV=gnu", "CURSES=yes", "all"]
    elif platform.system() == "Darwin":
        command += ["OS=macosx", "ENV=x86_64", "CURSES=yes", "all"]
    else:
        raise NotImplementedError(
            "Your OS is not supported at the moment, please install the CDF lib manually"
        )

    # run the command
    subprocess.check_call(command)


def install_cdf(raw_cdf_version, install_dir):
    # reformat the cdf version from X.Y.Z to XY_Z
    X, Y, Z = raw_cdf_version.split(".")
    cdf_version = f"{X}{Y}_{Z}"

    current_dir = os.path.abspath(os.path.join(install_dir, "current"))

    # prepare the make command
    command = [
        "make",
        "-C",
        os.path.join(install_dir, f"cdf{cdf_version}-dist"),
        f"INSTALLDIR={current_dir}",
        "install",
    ]

    # run the command
    subprocess.check_call(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("cdf_version", help="Version of the CDF to retrieve.")
    parser.add_argument(
        "-i",
        "--install-dir",
        help="Local directory where IDB source files will be saved",
    )
    parser.add_argument(
        "-c",
        "--cdf-url",
        help="URL or local path of the NASA CDF dist. source tar.gz file",
        default=default_cdf_url,
    )
    parser.add_argument(
        "--make",
        action="store_true",
        default=False,
        help="If passed, then build and install the CDF software",
    )

    args = parser.parse_args()

    get_cdf(args.cdf_version, args.install_dir, args.cdf_url)

    if args.make:
        make_cdf(args.cdf_version, args.install_dir)
        install_cdf(args.cdf_version, args.install_dir)
