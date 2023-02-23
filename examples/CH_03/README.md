# Chapter 3 Example Programs

This directory contains the Chapter 3 examples from the book and scripts to install and run those examples.

## Installation

You will need a Python virtual environment to run the programs so that any modules installed by the setup won't interfere with your system Python. The instructions here depend on having the `pyenv` utility installed on your system. To activate a Python virtual environment in this directory take the following steps:

```console
$ cd CH_03
$ pyenv local 3.10.3
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
```

Once you have a local Python virtual environment activated your command prompt should be prefixed with `(.venv)`. This indicates the Python system in the current directory is active and ready to run.

## Example Programs

- 01 - demonstrates a function splitting a string name into it's component parts
- 02 - demonstrates the single responsibility pattern
- 03 - demonstrates side effects of passing parameters by reference
