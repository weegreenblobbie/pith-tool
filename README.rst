pith
====

A simple command-line tool to execute Python while taking care of the
`PYTHONPATH`.


How does pith solve import issues?
==================================

`pith` is meant to be used inside a working copy of a Python package that is
under development.  Suppose you have a workspace with the following
directories::

    my_working_copy/
        module_a/
            fun_1.py
            fun_2.py
        module_b/
            fun_3.py
        module_c/
            fun_4.py    # uses fun_1, 2, and 3
        runscripts/
            nhilton/
                run_batch_job.py  # may use any of the modulues
                                  # including external ones in git_submodules
        git_submodules/
            external_workspace/
                external_module/
                    extra_fun.py

With all the different modules, unittests, and run scripts, coming up with the
approach for getting the imports correct can be difficult.

The `setpaths.py` anti-pattern
------------------------------

At my place of work, we develop complex tools that have evolved into many
submodules and packages.  The `runscripts` folder contains many scripts that
launch servers and batch process data.

Suppose there is a script several folders deep in `runscripts`::

    runscripts/nhilton/run_batch_job.py

How should this script manipulate the `PYTHONPATH` so that the script can write:

.. code-block:: python

    import module_a.fun_1
    import module_b.fun_3

My place of work uses make/scons to generate a set of `setpaths.py` in each of
the `runscripts` sub folders, whose purpose is the manipulate the `PYTHONPATH`
so that the imports work::

.. code-block:: python

    import setpaths        # manipulates sys.path
    import module_a.fun_1  # now these imports work
    import module_b.fun_3

This is an anti-pattern!  It's complicated, requires a build system to generate,
requires developers to remember to add 'import setpaths', and in the correct
order.

The solution: `pith`
====================

`pith` removes the need to manipulate the `PYTHONPATH` from inside a runscript
or unittest.  Instead, `pith` works by launching the python interpreter from
the root of the workspace and use module names:

.. code-block:: console

    # in BASH, use tab to auto-complete!
    $ pith runscripts/nhilton/run_batch_job.py
    Entering directory: /some/root/path/of/workspace
    python3 -m runscripts.nhilton.run_batch_job
    # ...

Even better, if you are in a sub directory, there's no need to `cd` up first:

.. code-block:: console

    $ pwd
    /some/root/path/of/workspace/runscripts/nhilton     # some deep sub folder
    $ pith run_batch_job.py
    Entering directory: /some/root/path/of/workspace    # the same as before
    python3 -m runscripts.nhilton.run_batch_job

By executing the code in the root of the workspace, you will always get
consistent import behavior.

This is especially useful if you are inside a unittest folder and want to run
just in a single test module.  Normally one would need to do this:

.. code-block:: console

    $ cd ../../to/root/of/workspace
    python3 -m unittests discover -p "*test_mytests*"

With `pith`, you just give it the .py filename:

.. code-blocK:: console

    $ pith test_fun.py
    Entering directory: /some/root/path/of/workspace
    python3 -m unittests module_a.tests.test_fun

You can even specify a specific test:

.. code-block:: console

    $ pith test_fun.Test1
    Entering directory: /some/root/path/of/workspace
    python3 -m unittests module_a.tests.test_fun.Test1
    # Only Test1 executes

How does pith work?
===================

`pith` looks for a config file called `.pithrc`, if it doesn't find it in the
the current path, it looks in the directory above.  It keeps going up until it
finds the `.pithrc`.  If you place it in the root of your workspace, then `pith`
will launch the configured python interpreter with the configured `PYTHONPATH`
from the directory.

Using the `.pithrc` allows flexiblal configuration and puts all the
`PYTHONPATH` in just a single file.

.pithrc Syntax
--------------

The `.pithrc` file is parsed using Python's ConfigParser.  There curerntly is
only one section:

    [pith]

The following are the allowed key value pairs

=========================  ===================================
Key                        Value Description
=========================  ===================================
echo                       Echo the full python command to the terminal (true)
interpreter                The python executable to use (python)
test_prefix                The prefix to check if a .py file is a unit test (test)
verbose                    Echo lots of information as pith executes (true)
pythonpath                 A string of paths to include in the `PYTHONPATH`, relative paths are okay, one per line
=========================  ===================================
