#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__file__)

try:
    from spacepy.pycdf import CDF, zAttr
except:
    logger.debug("spacepy not available, use local pycdf version!")
    from .cdf import *

# vim: set tw=79 :
