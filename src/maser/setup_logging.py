#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""maser4py logging setup module."""

import logging

__all__ = ["setup_logging"]


def set_level(logger_or_handler, quiet=False, debug=False):
    if debug:
        logger_or_handler.setLevel(logging.DEBUG)
    elif quiet:
        logger_or_handler.setLevel(logging.CRITICAL + 10)
    else:
        logger_or_handler.setLevel(logging.INFO)


def set_handler_config(handler, quiet=False, debug=False, formatter=None):
    set_level(handler, quiet=quiet, debug=debug)
    if formatter:
        handler.setFormatter(formatter)


def setup_logging(
    filename=None, quiet=False, debug=False, logger=logging.root, stream=None
):
    """Method to set up logging."""

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # set the logger log-level
    set_level(logger, quiet=quiet, debug=debug)

    # if no handler is provided
    if stream is None:
        # and no handler already exists
        if not logger.handlers:
            # set a default stream handler
            logger.addHandler(logging.StreamHandler())
    else:
        # add the given stream handler
        logger.addHandler(stream)

    # loop over existing handlers and set the config
    for handler in logger.handlers:
        set_handler_config(handler, quiet=quiet, debug=debug, formatter=formatter)

    # create the file handler
    if filename:
        fh = logging.FileHandler(filename, delay=True)
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s %(name)-\
                        12s %(levelname)-8s %(funcName)-12s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        if debug:
            fh.setLevel(logging.DEBUG)
        else:
            fh.setLevel(logging.INFO)

        logger.addHandler(fh)

    return logger
