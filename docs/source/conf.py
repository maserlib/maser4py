# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from pathlib import Path
import tomli

import sphinx_rtd_theme  # noqa: F401

ROOT_DIR = Path(__file__).parents[2]


def get_project_info():
    with open(ROOT_DIR / "pyproject.toml", "rb") as f:
        project_info = tomli.load(f)

    return project_info


project_info = get_project_info()

# -- Project information -----------------------------------------------------

project = project_info["tool"]["poetry"]["name"]
copyright = "2022, " + ", ".join(project_info["tool"]["poetry"]["authors"])
author = ", ".join(project_info["tool"]["poetry"]["authors"])


# The full version, including alpha/beta/rc tags
release = project_info["tool"]["poetry"]["version"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "recommonmark",  # markdown
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",  # google-like docstrings
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

autodoc_mock_imports = []

autosummary_generate = True
