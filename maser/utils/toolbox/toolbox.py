#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Toolbox module for maser-py package."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import os.path as osp
import re
import logging
import subprocess
import urllib.request
import traceback
import shutil
import errno

import tempfile

__all__ = ['get_version',
           'print_exception',
           'which',
           'truncate_str',
           'Singleton',
           'download_data',
           'setup_logging',
           'quote', 'uniq',
           'insert_char',
           'run_command',
           'move_safe']

# ________________ HEADER _________________________

# # Mandatory
# __version__ = ""
# __author__ = ""
# __date__ = ""
#
# # Optional
# __institute__ = ""
# __project__ = ""
# __license__ = ""
# __credit__ = [""]
# __maintainer__ = ""
# __email__ = ""
# __change__ = {"version": "change"}

# ________________ Global Variables _____________
# (define here the global variables)
LOGGER = logging.getLogger(__name__)

DEF_INDENT = ' ' * 16

# ________________ Class Definition __________
# (If required, define here classes)


class Singleton(type):
    """
    Singleton class.

    A metaclass to create singletons, i.e classes that can have at most only
    one instance created at a given time.
    """

    def __call__(cls, *args, **kwargs):
        """
        Singleton.__call__.

        Check that an instance is already
        stored before creating a new one.
        """
        if hasattr(cls, 'instance'):
            return cls.instance

        cls.instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.instance


# ________________ Global Functions __________
# (If required, define here global functions)

def get_version(changelog):
    """Get latest version from the input CHANGELOG.md file."""
    pattern = re.compile(r'(\d*)\.(\w*)\.(\w*)')
    if osp.isfile(changelog):
        with open(changelog, 'rt') as file:
            for line in file:
                if pattern.match(line):
                    return line.strip()

    print('WARNING: CHANGELOG.md not found or invalid, version unknown!')
    return 'unknown'



def move_safe(src, dst,
              no_erase=False,
              tempdir=tempfile.gettempdir()):
    """
    Safely move a sections file or a directory into a dst directory.

    If no_erase keyword is True, then do no delete the original file/folder
    but move it to a tempdir in case of.
    """
    # Build target file/folder
    target = os.path.join(dst, os.path.basename(src))

    # copy file/folder
    try:
        shutil.copytree(src, target)
        is_item = os.path.isdir
    except shutil.Error as e:
        LOGGER.error('Directory not copied. Error: %s'.format(e))
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copyfile(src, dst)
            is_item = os.path.isfile
        else:
            LOGGER.error('{0} is not a valid directory!'.format(dst))
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), src)

    # Check that file/directory has been correctly copied before removing the
    # original
    if not is_item(target):
        LOGGER.error(
            '{0} has not been moved correctly, aborting!'.format(src))
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), src)

    if no_erase:
        move_safe(src, tempdir)
        LOGGER.info('{0} moved in {1}'.format(src, tempdir))

    return target


def download_data(url,
                  encoding='utf-8',
                  target_file=None,
                  binary=False):
    """Download the data from the given url.

    If target_file input keyword is not None, then
    save data into the target_file path.
    """
    try:
        buff = urllib.request.urlopen(url)
        data = buff.read().decode(encoding)
    except:
        return None
    else:
        if target_file is not None:
            if binary:
                wm = 'wb'
            else:
                wm = 'w'
            with open(target_file, wm) as fw:
                fw.write(data)
    return data


def insert_char(string, char, pos):
    """Insert substring in a string."""
    return string[:pos] + char + string[pos:]


def print_exception(message=None, exit=True):
    """
    Print_exception.

    To handle the printing of the error message when one occurred. Particularly
    useful when catching errors and want to add debug informations on the same
    time.
    """
    # get the traceback
    trace = traceback.format_exc()

    # if not message provided, get the traceback of errors to be a little more
    # useful for the developer
    if message is not None:
        mess = '\n'.join([trace, message])
    else:
        # else use message provided by developer
        mess = trace

    # show error in the logger
    LOGGER.error(mess)

    if exit:
        sys.exit(1)

    # return the message
    return mess


def quote(string, unquote=False):
    """Double quote a given string."""
    if string is not None:
        if not isinstance(string, str):
            string = str(string)
        if string.startswith("\""):
            string = string[1:]
        if string.endswith("\""):
            string = string[:-1]
        if unquote:
            return string
        return "\"" + string + "\""


def run_command(cmd, env=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                logger=LOGGER):
    """Run a command with subprocess."""

    try:
        logger.info(' '.join(cmd))
        res = subprocess.Popen(cmd, env=env, shell=shell,
                               stdout=stdout,
                               stderr=stderr)
    except TypeError as e:
        logger.error(e)
    except OSError as e:
        logger.error(e)
    except subprocess.TimeoutExpired as e:
        logger.error('TIME OUT EXPIRED:  %i SEC.', e.timeout)

    return res


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


def setup_logging(filename=None,
                  quiet=False, debug=False,
                  logger=logging.root,
                  stream=None):
    """Method to set up logging."""

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')


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
        fh.setFormatter(logging.Formatter('%(asctime)s %(name)-\
                        12s %(levelname)-8s %(funcName)-12s %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S'))
        if debug:
            fh.setLevel(logging.DEBUG)
        else:
            fh.setLevel(logging.INFO)

        logger.addHandler(fh)

    return logger


def truncate_str(string, max_length,
                 gap=DEF_INDENT,
                 min_length=3):
    """Truncate a too long CDF_CHAR value."""
    nstr = len(string)
    new_string = ''
    for i, val_c in enumerate(string):
        if i > nstr - min_length:
            new_string += string[i:]
            break
        new_string += val_c
        if (i % max_length == 0) and (i != 0):
            new_string += "\" - \n" + gap + "\""

    return new_string


def uniq(seq, not_none=False):
    """Get list of unique elements from an input sequence of list type."""
    seen = set()
    seen_add = seen.add
    if not_none:
        return [x for x in seq if not (x in seen or seen_add(x) or x is None)]
    else:
        return [x for x in seq if not (x in seen or seen_add(x))]


def which(program, path='PATH'):
    """Run which function."""
    def is_exe(fpath):
        """Run is_exe function."""
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, __ = os.path.split(program)

    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ[path].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


# _________________ Main ____________________________
if __name__ == '__main__':
    print('toolbox for maser package')
