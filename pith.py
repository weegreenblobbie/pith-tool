#!/usr/bin/env python

"""
pith tool

A simple command-line tool to execute Python while taking care of the PYTHONPATH.

See https://github.com/weegreenblobbie/pith-tool
"""

import ConfigParser
import glob
import os
import platform
import subprocess
import sys


def main():

    run_dir = os.getcwd()

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

    # defaults

    echo = True
    path_str = ''
    py_exe = 'python'
    test_prefix = 'test'
    verbose = True

    config = read_pithrc(pith_rc)

    try:
        echo = config.getboolean('pithrc', 'echo')
    except ConfigParser.NoOptionError:
        pass

    try:
        path_str = config.get('pithrc', 'pythonpath')
    except ConfigParser.NoOptionError:
        pass

    try:
        py_exe = config.get('pithrc', 'interpreter')
    except ConfigParser.NoOptionError:
        pass

    try:
        test_prefix = config.get('pithrc', 'test_prefix').strip()
    except ConfigParser.NoOptionError:
        pass

    try:
        verbose = config.getboolean('pithrc', 'verbose')
    except ConfigParser.NoOptionError:
        pass

    python_path = parse_python_path(root_dir, path_str)

    if verbose:
        print_settings(root_dir, py_exe, python_path)

    #--------------------------------------------------------------------------
    # handle no arguments, dump setttings and exit

    if len(sys.argv) == 1:

        # nothing to do, report settings (if not already reported) and exit

        if not verbose:
            print_settings(root_dir, py_exe, python_path)

        print("Nothing to do!")

        sys.exit(1)

    #--------------------------------------------------------------------------
    # setup PYTHONPATH in env

    path_sep = ':'

    if 'win32' in platform.system():
        path_sep = ';'

    ppaths = path_sep.join(python_path)

    env = os.environ.copy()
    env['PYTHONPATH'] = ppaths

    #--------------------------------------------------------------------------
    # get command line arguments

    args, paths = make_py_commnad(root_dir, run_dir, test_prefix)

    cmd = [py_exe]
    cmd.extend(args)

    #--------------------------------------------------------------------------
    # python3 doesn't require __init__.py files to be everywhere
    # python2 does.

    ver = subprocess.check_output(
        [py_exe, '--version'], stderr=subprocess.STDOUT)

    is_py2 = 'Python 2.' in ver

    init_files = []

    if is_py2:
        init_files = make_init_py_files(paths, verbose)

    #--------------------------------------------------------------------------
    # finally, execute python

    # show the command unless echo is disabled

    if echo:

        if not verbose:
            print('Entering directory: %s' % root_dir)

        print(" ".join(cmd))

    if is_py2 and len(init_files) > 0:

        reraise = False

        try:
            subprocess.check_call(cmd, env = env)
        except:
            reraise = True

        # clean up __init__.py files
        cleanup_init_file(init_files, verbose)

        if reraise:
            raise

    else:
        subprocess.check_call(cmd, env = env)


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


def make_py_commnad(root_dir, run_dir, test_prefix):
    """
    gobble up sys.argv and transform into propery python module command.
    """

    # run_dir must start with root dir

    if not run_dir.startswith(root_dir):
        raise RuntimeError("oops, what's going on:\n%s\n%s\n" % (
            root_dir, run_dir)
        )

#~    run_dir = run_dir[len(root_dir) + 1 :]

    args = []
    paths = []

    found_script = False

    for arg in sys.argv[1:]:

        dot_py = arg.endswith('.py')
        is_test = os.path.basename(arg).startswith(test_prefix)

        if not found_script and (dot_py or is_test):

            # abspath here to remove possible '/../../'
            arg = os.path.abspath(os.path.join(run_dir, arg))

            # strip off root_dir

            arg = arg[len(root_dir) + 1 :]

            # pull off .py
            if dot_py:
                [arg, _] = os.path.splitext(arg)

            mod = arg.replace(os.path.sep, '.')

            if is_test:
                args.extend(['-m', 'unittest', mod])
            else:
                args.extend(['-m', mod])

            found_script = True

            # save the paths to this script so for python2, temporary
            # __init__.py files can be created

            dirname = os.path.dirname(arg)

            while len(dirname) > 0:
                paths.append(dirname)
                dirname = os.path.dirname(dirname)

        else:
            args.append(arg)

    return args, paths


def make_init_py_files(paths, verbose):
    """
    For each path, if __init__.py doesn't exist write out a temporary one.
    """

    filelist = []

    for p in paths:

        init = os.path.join(p, '__init__.py')

        if not os.path.isfile(init):

            filelist.append(init)

            if verbose:
                print('Touching %s' % init)

            with open(init, 'w') as fd:
                fd.write('')

    return filelist


def cleanup_init_file(init_files, verbose):

    for init in init_files:

        filelist = glob.glob(init + '*') # pick up .pyc and .pyo extensions

        for f in filelist:

            if verbose:
                print('Cleaning up %s' % f)

            os.remove(f)


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