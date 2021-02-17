#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Contains exceptions for the cdf module.

"""

import logging

logger = logging.getLogger(__name__)

__all__ = ['InvalidFile', 'InvalidSkeleton',
           'InvalidEntry', 'CDFSerializerError']

class InvalidFile(Exception):
    """Exception raise if the input file is invalid."""

    def __init__(self, message='', *args, **kwargs):
        super(InvalidFile, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

class InvalidSkeleton(Exception):
    pass

class InvalidEntry(Exception):
    def __init__(self, message='', *args, **kwargs):
        super(InvalidEntry, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class CDFSerializerError(Exception):
    pass
