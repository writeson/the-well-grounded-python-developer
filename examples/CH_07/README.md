# Chapter 7 Example Programs

This directory contains the Chapter 7 examples from the book and scripts to install and run those examples.

## Installation

You will need a Python virtual environment to run the programs so that any modules installed by the setup won't interfere with your system Python. The instructions here depend on having the `pyenv` utility installed on your system. To activate a Python virtual environment in this directory take the following steps:

```console
$ cd CH_07
$ pyenv local 3.10.3
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
```

Once you have a local Python virtual environment activated your command prompt should be prefixed with `(.venv)`. This indicates the Python system in the current directory is active and ready to run.

To install modules necessary for this chapter run the following command line with your Python virtual environment active:

```console
pip install -r requirements.txt
```

The command will pip install any modules necessary to run the example programs in the chapter and create shortcuts to run the example programs.

## Example Programs

- 01 modifies the web application to use Bootstrap for styling and a media query for responsive design of the banner
- 02 refactors the web application into a better, more scalable structure
- 03 refactors the web application to use Flask Blueprints
- 04 adds Bootstrap navbar navigation to the application, Flask Blueprints to modularize the app and an about page to demonstrate it.
- 05 adds the flask debug toolbar
- 06 adds Python logging to the MyBlog application
- 07 adds a favicon to the application and a brand graphic to the navigation bar
