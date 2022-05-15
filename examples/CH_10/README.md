# Chapter 10 Example Programs

This directory contains the Chapter 10 examples from the book and scripts to install and run those examples.

## Installation

You will need a Python virtual environment to run the programs so that any modules installed by the setup won't interfere with your system Python. The instructions here depend on having the `pyenv` utility installed on your system. To activate a Python virtual environment in this directory take the following steps:

```console
$ cd CH_10
$ pyenv local 3.10.3
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
```

Once you have a local Python virtual environment activated your command prompt should be prefixed with `(.venv)`. This indicates the Python system in the current directory is active and ready to run.

To install the modules necessary for this chapter run the following command line:

```console
pip install -r requirements.txt
```

## Example Programs

To run the example programs just enter the command line shortcut shown in the list below. The list below shows the shortcut command and a brief description of what the command does.

- 01 uses CSV files to provide data for an imaginary company and produce invoice PDF files for all the orders in the system
- 02 uses a SQLite database and SQLAlchemy to replicate the functionality of example 01
