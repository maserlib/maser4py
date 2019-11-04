#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp
import sys
import re

from setuptools import Command


class APIDoc(Command):
    """
    Create a specific command handler to generate and create the documentation
    of the program.
    """
    description = 'run sphinx-apidoc'
    user_options = []

    def initialize_options(self):
        """
        Set default values for options.
        """
        # Each user option must be listed here with their default value.
        pass

    def finalize_options(self):
        """
        Post-process options.
        """
        pass

    def run(self):
        from sphinx.apidoc import main
        """Run command."""
        # process options as done in the source file of sphinx
        sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])

        print(sys.argv[0])
        # create the absolute paths to where to put things to avoid problems
        sourcedir = osp.join(
            osp.dirname(osp.abspath(__file__)))
        buildir = osp.join(
            osp.dirname(osp.abspath(__file__)),
            "build")

        apidir = osp.join(sourcedir, "api")

        rootdir = osp.join(
            osp.dirname(osp.abspath(__file__)),
            osp.pardir)

        # same here, and add path
        main([
            'sphinx-apidoc', '-f', '-o',
            osp.join(apidir, "maser4py"),
            osp.join(rootdir, "maser"),
            "--separate",
        ])

        # build the documentation as provided by sphinx
        self.run_command("build_sphinx")
