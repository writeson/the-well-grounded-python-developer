# Chapter 6 Example Programs

This directory contains the Chapter 6 examples from the book and scripts to install and run those examples.

## Installation

You will need a Python virtual environment to run the programs so that any modules installed by the setup won't interfere with your system Python. The instructions here depend on having the `pyenv` utility installed on your system. To activate a Python virtual environment in this directory take the following steps:

```console
$ cd CH_06
$ pyenv local 3.10.3
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
```

Once you have a local Python virtual environment activated your command prompt should be prefixed with `(.venv)`. This indicates the Python system in the current directory is active and ready to run.

To install the modules necessary, for this chapter the following command line while your Python virtual environment is active:

```console
pip install -r requirements.txt
```

## Example Programs

- 01 - demonstrates a simple "Hello World" web application
- 02 - demonstrates a web application with dynamically updated data
- 03 - demonstrates a web application with dynamically updated data and user interactive