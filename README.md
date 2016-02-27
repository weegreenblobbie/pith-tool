pith
====

A simple command-line tool to execute Python while taking care of the PYTHONPATH.

How does pith solve import issues?
==================================

`pith` is meant to be used inside a working copy of a Python package that is
under development.  Suppose you have a workspace with the following directories:

    my_working_copy/
        module_a/
            fun_1.py
            fun_2.py
        module_b/
            fun_3.py
        module_c/
            fun_4.py    # uses fun_1, 2, and 3
        runscripts/
            run_examples.py  # may use any of the modulues
                             # including external ones in git_submodules
            bamboo/
                run_code_coverage.py
        git_submodules/
            3rd_party_repo/
                ...
        setup.py

With all the different modules, unittests, and run scripts, coming up with the
approach for getting the imports correct can be difficult.

## The `setpaths.py` anti-pattern

At my place of work, we develop complex tools that has evolved into many
submodules and packages.  The `runscripts` folder contains many scripts that
launch servies and batch process data.

Suppose there is a script several subfolders deep `runscripts`:

    runscripts/nhilton/run_batch_job.py

How should this script manipulate the PYTHONPATH so that the script can write:

    import module_a.fun_1
    import module_b.fun_3

My place of work uses make/scons to generate a set of `setpaths.py` in each of
the runscripts sub folders, whose pusrpose is the manipulate the PYTHONPATH so
that the imports work:

    import setpaths
    import module_a.fun_1
    import module_b.fun_3

This is an anti-pattern!  It's complicated, request a build system to generate,
requires developers to remember to 'import setpaths' in the correct place, may
get complicated if a local module is also importing a their own `setpaths`
modules.

## The solution: `pith`

`pith` remove the need to PYTHONPATH hacks like generated `setpaths`.  `pith` works
by always launching the python interpreter from the root of the workspace:

```bash
$ `pith` runscripts/nhilton/run_batch_job.py
Entering directory: /some/root/path/of/workspace
python3 -m runscripts.nhilton.run_batch_job
# ...
```

Even better, if you are in a subdirectory:

    $ cd runscripts/nhilton
    $ `pith` run_batch_job.py
    Entering directory: /some/root/path/of/workspace
    python3 -m runscripts.nhilton.run_batch_job

You will always get a consistent way to execute the script.  This is especially
useful if you are inside a unittest folder and want to run just the tests in
a single module.  Normally one would need to do this:

    $ cd ../../to/root/of/workspace
    python3 -m unittests discover -p "*test_mytests*"

With `pith` you can be in the unittest folder and just give it the .py filename:

    $ cd module_a/tests
    $ `pith` test_mytests.py
    Entering directory: /some/root/path/of/workspace
    python3 -m unittests -p module_a.tests.test_mytests

