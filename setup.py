"""
pith tool

A simple command-line tool to execute Python while taking care of the PYTHONPATH.

See https://github.com/weegreenblobbie/pith-tool
"""

from setuptools import setup, Extension

# README.rst processing

with open("README.rst") as fd:
    readme_rst = fd.read()

keywords = '''
    development
    command-line
    script
'''.split()

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Topic :: Utilities",
]

description = """\
A simple command-line tool to execute Python while taking care of the
PYTHONPATH.
"""

setup(
    author           = "Nick Hilton et al",
    author_email     = "weegreenblobbie@yahoo.com",
    classifiers      = classifiers,
    description      = description,
    keywords         = keywords,
    long_description = readme_rst,
    name             = "pith",
#~    py_modules       = [],
    scripts          = ['pith'],
    url              = "http://nsound.sourceforge.net",
    version          = "0.1",
)