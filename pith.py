#!/usr/bin/env python

"""
pith tool

A simple command-line tool to execute Python while taking care of the PYTHONPATH.

See https://github.com/weegreenblobbie/pith-tool
"""

import ConfigParser
import os
import sys


def main():

    #--------------------------------------------------------------------------
    # search for .pithrc

    pith_rc = scan_for_pithrc()

    if pith_rc is None:
        sys.stderr.write(
            "Could not find .pithrc, please create one with contents:\n%s\n" % (
                PITH_RC_TEMPLATE
            )
        )

        raise RuntimeError('Could not find .pithrc')

    root_dir = os.path.dirname(pith_rc)

    os.chdir(root_dir)

    #--------------------------------------------------------------------------
    # parse .pithrc

    config = read_pithrc(pith_rc)

    try:
        py_exe = config.get('pithrc', 'interpreter')

    except ConfigParser.NoOptionError:
        py_exe = 'python'

    try:
        verbose = config.get('pithrc', 'verbose').lower() == 'true'

    except ConfigParser.NoOptionError:
        verbose = True

    try:
        path_str = config.get('pithrc', 'pythonpath')

    except ConfigParser.NoOptionError:
        path_str = ''

    python_path = parse_python_path(root_dir, path_str)

    if verbose:
        print_settings(root_dir, py_exe, python_path)

    #--------------------------------------------------------------------------
    # handle arguments

    print "sys.argv = ", sys.argv

    if len(sys.argv) == 1:

        # nothing to do, report settings (if not already reported) and exit

        if not verbose:
            print_settings(root_dir, py_exe, python_path)
            sys.exit(1)


def scan_for_pithrc():

    cwd = os.path.abspath(os.getcwd())

    last_cwd = cwd

    while True:

        pith_rc = os.path.join(cwd, '.pithrc')

        if os.path.isfile(pith_rc):
            return pith_rc

        cwd = os.path.dirname(cwd)

        # no more path?

        if cwd == last_cwd:
            break

        last_cwd = cwd

    return None


def read_pithrc(pith_rc):

    config = ConfigParser.SafeConfigParser()
    config.read(pith_rc)

    return config


def parse_python_path(root_dir, path_str):
    """
    The incoming python string should be a string seperated by newlines:

        "\n../nsound/nsound_git_ws\n../nsound/nsound_git_ws2"

    This should should become a list of strings of absolute paths.
    """

    paths = path_str.strip().split('\n')

    python_path = [root_dir]

    for p in paths:
        p = p.strip()

        # p may be a relative path, convert to abs

        abs_p = os.path.abspath(p)

        if not os.path.isdir(abs_p):
            raise RuntimeError(
                "While parsing .pithrc pythonpath, could not find path: %s" % p
            )

        python_path.append(abs_p)

    return python_path


def print_settings(root_dir, py_exe, python_path):
    print('Entering directory: %s' % root_dir)
    print('Python interpreter: %s' % py_exe)

    if len(python_path) > 0:
        print('PYTHONPATH:')

    for p in python_path:
        print('    %s' % p)


#------------------------------------------------------------------------------
# globals

PITH_RC_TEMPLATE = """\
[pithrc]

interpreter = python

pythonpath =

verbose = true

"""



if __name__ == "__main__":
    main()