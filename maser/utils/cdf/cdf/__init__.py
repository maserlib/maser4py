#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__file__)

try:
    from spacepy.pycdf import *
except:
    logger.warning("spacepy not available, use local pycdf version!")
    from maser.utils.cdf.cdf.cdf import *
