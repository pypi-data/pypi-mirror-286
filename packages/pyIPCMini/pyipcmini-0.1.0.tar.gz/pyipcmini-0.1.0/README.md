# pyIPCMini

pyIPCMini is a package to communicate and control via USB/serial the ion pump controller type IPCMini from Agilent.

It has been tested using the RS232 protocol, with the pump's DB9 connector hooked to a USB-serial converter based on FTDI chip.

This is an unofficial package for the [IPCMini](https://www.agilent.com/en/product/vacuum-technologies/ion-pumps-controllers/ion-pump-controllers/ipcmini-ion-pump-controller) and it is not supported by the equipment's vendor.

## Installation

You can install this package from PyPI, using the following command:

    pip install pyIPCMini

Alternatively, you can clone the latest version from github:

    git clone https://github.com/benjaminpasquiou/pyIPCMini.git


## Usage

### Python package

For starting using this package, you can see these [useful examples](https://github.com/benjaminpasquiou/pyIPCMini/blob/main/notebooks/Examples.ipynb).

You can also look into the [package documentation](https://pyIPCMini.readthedocs.io).

### Application

For using the application on the command line, to see the help message, you can first use:

    pyIPCMini -h

An example of a working command:

    pyIPCMini -p "/dev/ttyUSB0" -l "My pump" --show

The application's functionalities are very limited and are just examples for you to build on and obtain something that matches your needs.
You then would have to use a combination of *python -m build -- wheel* and *python -m pip install pyIPCMini-X.X.X-py3-none-any.whl* within the python environment of your choice, to install your own modified version of the application.

## Warning

An ion pump is a sensitive device, and if not used properly it can potentially cause harm to the user, to the device itself, or to other pieces of equipment. This package should only be used by trained operators. Please read Agilent IPCMini's manual and make sure that you can safely operate the pump in manual mode, before using the package for remote control. Please also consult the package's documentation at [https://pyIPCMini.readthedocs.io](https://pyIPCMini.readthedocs.io) before using any of its functionalities. Also, let me reminds you of no-liability statement in the package's [license](https://github.com/benjaminpasquiou/pyIPCMini/blob/main/LICENSE).
