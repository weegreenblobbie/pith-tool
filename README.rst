pith
====

A simple command-line tool to execute Python while taking care of the
``PYTHONPATH``.


How does pith solve import issues?
==================================

``pith`` is meant to be used inside a working copy of a Python package that is
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

The ``setpaths.py`` anti-pattern
--------------------------------

At my workplace, we develop complex tools that have evolved into many
submodules and packages.  The ``runscripts`` folder contains many scripts that
launch servers and batch process data.

Suppose there is a script several folders deep in ``runscripts``::

    runscripts/nhilton/run_batch_job.py

How should this script manipulate the ``PYTHONPATH`` so that these imports work?

.. code-block:: python

    import module_a.fun_1
    import module_b.fun_3

My workplace uses make/scons to generate a set of ``setpaths.py`` helper
modules that manipulate the ``PYTHONPATH``, each one is different because each
one is in a different directory.  The ``setpaths.py`` module manipulates
``sys.path`` so the imports work:

.. code-block:: python

    import setpaths        # manipulates sys.path
    import module_a.fun_1  # now these imports work
    import module_b.fun_3

This is an anti-pattern!  The following all have to be done:

* Requires a build system
* Requires developers to execute the build system command before running
* Requires the maintenance of the ``setpaths.py`` templates
* Requires developers to add ``import setpaths`` in the correct place in their code

The solution: ``pith``
======================

``pith`` removes the need to manipulate the ``PYTHONPATH`` from inside a runscript
or unittest.  Instead, ``pith`` works by launching the python interpreter from
the root of the workspace:

.. code-block:: console

    # in BASH, use tab to auto-complete!
    $ pith runscripts/nhilton/run_batch_job.py
    Entering directory: /some/root/path/of/workspace
    python3 -m runscripts.nhilton.run_batch_job
    # ...

Even better, if you are in a sub directory, there's no need to ``cd`` up first:

.. code-block:: console

    $ pwd
    /some/root/path/of/workspace/runscripts/nhilton     # some deep sub folder
    $ pith run_batch_job.py
    Entering directory: /some/root/path/of/workspace    # the same as before
    python3 -m runscripts.nhilton.run_batch_job

By executing Python from the root of the workspace, you will always get
consistent import behavior.  In addition, there is now only one place to
configure the ``PYTHONPATH``, which reduces complexity and maintenance.

``pith`` is especially useful if you want to execute unit tests from deep inside
the module's folder.  Normally one would need to do this:

.. code-block:: console

    $ cd ../../to/root/of/workspace
    python3 -m unittests discover -p "*test_mytests*"

With ``pith``, you can remain the the folder and just specify the ``.py`` filename:

.. code-blocK:: console

    $ pith test_fun.py
    Entering directory: /some/root/path/of/workspace
    python3 -m unittests module_a.tests.test_fun

You can even specify a specific test and test function:

.. code-block:: console

    $ pith test_fun.Test2.test_01
    Entering directory: /some/root/path/of/workspace
    python3 -m unittests module_a.tests.test_fun.Test2.test_01
    # Only test_fun.Test2.test_01 executes

How does pith work?
===================

``pith`` looks for a config file called ``.pithrc``, if it doesn't find it in the
the current directory, it looks in the directory above.  It keeps going up
until it finds a ``.pithrc``.  If you place it in the root of your workspace,
then ``pith`` will launch the configured Python interpreter with the configured
``PYTHONPATH`` from the root of the workspace.

Using the ``.pithrc`` allows flexible configuration and puts all the ``PYTHONPATH``
specification in a single file.

``.pithrc`` Syntax
------------------

The ``.pithrc`` file is parsed using Python's ConfigParser.  Currently the only
section is::

    [pith]

The following are the allowed key value pairs

=========================  ===================================
Key                        Value Description
=========================  ===================================
echo                       Echo the full python command to the terminal (default = true)
interpreter                The python executable to use (default = python)
test_prefix                The prefix to check if a .py file is a unit test (default = test)
verbose                    Echo lots of information as pith executes (default = true)
pythonpath                 A string of paths to include in the ``PYTHONPATH``, relative paths are okay, one per line (no default)
=========================  ===================================

Example ``.pithrc`` file
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

    [pith]

    interpreter = python

    echo = 1
    verbose = 1

    # additional paths, 1 per line

    pythonpath =
        git_submodules/external_workspace


See the ``example`` directory in this repo with a toy project that matches the
examples in this README.