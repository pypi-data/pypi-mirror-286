# SU stdlibs for Python 3

`su-stdlibs-python` is an adapted version of the [Python programs](https://introcs.cs.princeton.edu/python/code/) provided with the textbook [Introduction to Programming in Python](https://introcs.cs.princeton.edu/python/home/) by Sedgewick, Wayne, and Dondero.

<!-- [![Build Status](https://github.com/bongomarcel/su-stdlibs-python/workflows/check/badge.svg)](https://github.com/bongomarcel/su-stdlibs-python/actions)
[![Documentation Status](https://readthedocs.org/projects/sustdlibspython/badge/?version=latest)](https://sustdlibspython.readthedocs.io/en/latest/?badge=latest) -->

## Target audience

`su-stdlibs-python` is intended for instructors and students who wish to follow the textbook [Introduction to Programming in Python, 1st Edition](https://introcs.cs.princeton.edu/python/home/) by Sedgewick, Wayne, and Dondero.
It was first created in 2023 by teaching assistants and instructors at [Stellenbosch University](https://cs.sun.ac.za).

## Installation

This library requires a functioning Python 3 environment.

Some optional visual and auditory features depend on the [numpy](http://numpy.org) and [pygame](https://pygame.org) packages.

### With pip
For Python versions 3.8 - 3.10, due to compatability infeasibilities, the current safest option is to install most requirements manually before installing this package.

```bash
python3 -m pip --upgrade pip
python3 -m pip --upgrade wheel
python3 -m pip --upgrade setuptools
python3 -m pip --upgrade numpy
python3 -m pip --upgrade pygame
python3 -m pip --upgrade mypy
```

After the above commands execute sucessfully, install `su-stdlibs-python` simply with
```bash
python3 -m pip install --upgrade su-stdlibs-python
```

To test that you have installed the library correctly, run this command:
```bash
python3 -c 'import stdio; stdio.write("Hello World!\n")'
```
It should greet you. If an error message appears instead, the library is not installed correctly.

<!-- ### Alternative: With pip and git

If git is available, the following command will install the library in your Python environment:

```bash
python3 -m pip install git+https://github.com/bongomarcel/su-stdlibs-python
```

### Alternative: With pip and zip

To install this library without git:

1. Download and unzip the repository.
2. Open a command prompt or terminal and navigate to the downloaded folder. There should be the file `setup.py`.
3. Use the command `pip3 install .` to install the package (this will also work for updating the package, when a newer version is available).  If your Python installation is system-wide, use `sudo pip3 install .`

### Alternative: Step-by-step guide for Windows

To install the Python package `su-stdlibs-python`:

- Download the repository by pressing the green "Clone or download" button, and pressing "Download ZIP".
- Extract the content of the zip to your Desktop (you can delete the folder after installing the package).
- Open the "Command Prompt" by pressing "Windows + R", type "cmd" in the window that appears, and press "OK".
- If you saved the folder on the Desktop you should be able to navigate to the folder by typing "cd Desktop\itu.algs4-master".
```
C:\Users\user>cd Desktop\su-stdlibs-python-master
```
- When in the correct folder, type `pip install .` to install the package. 
```
C:\Users\user\Desktop\su-stdlibs-python-master>pip install .
```
- After this, the package should be installed correctly and you can delete the folder from your Desktop.

## Examples

The directory [examples/](examples) contains examples, some of which are
described here. -->

### Hello World
A simple program, stored as a file [hello_world.py](examples/hello_world.py), looks like this:
```python
import stdio

stdio.write("Hello World!\n")
```
It can be run with the command `python3 hello_world.py`.

## How to suppress pygame import message
### Windows
In the command line enter the following and hit enter:
```bash
set PYGAME_HIDE_SUPPORT_PROMPT="1"
```
### Linux
In the terminal enter the following and hit enter:
```bash
export PYGAME_HIDE_SUPPORT_PROMPT=1
```

### In-code
In your code add the following to the beginning of your code.
```python
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame  # it is important to import pygame directly after
```

<!-- ## Documentation

The documentation can be found [here](https://sustdlibspython.readthedocs.io/en/latest/).

## Development

`su-stdlibs-python` has known bugs and has not been tested systematically. We are open to pull requests, and in particular, we appreciate the contribution of high-quality test cases, bug-fixes, and coding style improvements. -->

## Contributors

- Marcel Dunaiski

## License

This project is licensed. See the [LICENSE](LICENSE) file for details.