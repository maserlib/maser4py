# -*- coding: utf-8 -*-
import struct


def _merge_dtype(dtypes):
    return dtypes[0] + "".join(dt[1:] for dt in dtypes[1:])


def _read_sweep_length(file):
    block = file.read(4)
    if len(block) == 0:
        return None
    else:
        return struct.unpack(">i", block)[0]
