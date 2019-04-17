#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ________________ HEADER _________________________


"""
Contains exceptions for the cdf module.

"""

__all__ = ["InvalidFile", "InvalidSkeleton", "SkeletonCDFException"]

class InvalidFile(Exception):
    pass

class InvalidSkeleton(Exception):
    pass

class SkeletonCDFException(Exception):
    pass