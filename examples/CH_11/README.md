# Chapter 11 Example Programs

This directory contains the Chapter 11 examples from the book and scripts to install and run those examples.

## Installation

You will need a Python virtual environment to run the programs so that any modules installed by the setup won't interfere with your system Python. The instructions here depend on having the `pyenv` utility installed on your system. To activate a Python virtual environment in this directory take the following steps:

```console
$ cd CH_09
$ pyenv local 3.9.6
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
```

Once you have a local Python virtual environment activated your command prompt should be prefixed with `(.venv)`. This indicates the Python virtual environment in the current directory is active and ready to run.

To install the modules necessary for this chapter run the following command line with your Python virtual environment active:

```console
pip install -r requirements.txt
```

The command will pip install any modules necessary to run the example programs in the chapter and create shortcuts to run the example programs.

## Example Programs

- Example 01 Adds the ability to create content posts using markdown syntax
