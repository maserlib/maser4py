# -*- coding: utf-8 -*-
import struct


def _merge_dtype(dtypes):
    return dtypes[0] + "".join(dt[1:] for dt in dtypes[1:])


def _read_sweep_length(file):
    sweep_length = _read_block(file, ">i")
    return sweep_length[0] if sweep_length is not None else None


def _read_block(file, dtype, fields=None):
    block_len = struct.calcsize(dtype)
    block = file.read(block_len)
    if len(block) == 0:
        return None
    else:
        if fields is None:
            return struct.unpack(dtype, block)
        else:
            return dict(zip(fields, struct.unpack(dtype, block)))
