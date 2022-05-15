# The Well-Grounded Python Developer

## Introduction

This repository contains the example code that accompanies the book. The code is organized under an `examples` root file. Each chapter has its own directory, and all of the examples for that chapter (if it has any) have one of two styles:

* Python file named XX.py if the entire example is in a single file
* CH_XX as a directory name if the example code consists of multiple files in that directory

## General Installation

Because this is a repository of Python code, you need to have Python installed on your computer. Preferably this would use the `pyenv` tool. This tool allows you to install multiple versions of Python if you'd like, but more importantly it doesn't interfere with the system installed version if it exists.

On a Mac, the easiest way to install pyenv is to use Homebrew. This is what's recommended at this link, which describes how to install it for all environments. Here is the link to get [pyenv](https://github.com/pyenv/pyenv)

After getting pyenv installed, run this command: ```pyenv install 3.10.3```

Follow these steps to install and setup the repository:

1. Create a directory where you want this repository to exist
2. cd into that directory
3. Run this git command: ```git clone https://github.com/writeson/the_well_grounded_python_developer_code.git```

## Chapter Installation

Where necessary, each chapter has it's own `README.md` file that explains how to install any modules needed by the example programs in that chapter.
