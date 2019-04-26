#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""
Contains exceptions for the cdf module.

"""

__all__ = ["InvalidFile", "InvalidSkeleton",
           "InvalidEntry", "CDFSerializerError"]

class InvalidFile(Exception):
    pass

class InvalidSkeleton(Exception):
    pass

class InvalidEntry(Exception):
    pass

class CDFSerializerError(Exception):
    pass