##########################################################################################
#
# Example script to communicate with an Agilent IPCMini ion pump controller via RS232 serial.
#
##########################################################################################
"""Example script to communicate with an Agilent IPCMini ion pump controller via RS232 serial."""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import pyipcmini


def save_measured_values(pressure: float, current: float, path: str = ".") -> None:
    """Save values in csv file."""
    filename = path + "/" + "pump_readings.csv"
    with Path(filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Pressure", pressure])
        writer.writerow(["Current", current])


def main() -> None:
    """Start main."""
    parser = argparse.ArgumentParser(description="IPCMini handler")
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        help="com port for USB/serial connection",
        default="/dev/ttyUSB0",
    )
    parser.add_argument(
        "-b",
        "--baud",
        type=int,
        help="baud rate for USB/serial connection",
        default=9600,
    )
    parser.add_argument(
        "-l",
        "--label",
        type=str,
        help="label of the pump",
        required=True,
    )
    parser.add_argument(
        "--path",
        type=str,
        help="path where to store the results",
        default=".",
    )
    parser.add_argument(
        "--show",
        help="show the results instead of saving them",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--cmd",
        type=str,
        help="apply command to ion pump controller",
        default="None",
        choices=["None", "HV ON/OFF", "V target"],
    )
    args = parser.parse_args()

    port = args.port
    baud = args.baud
    lbl = args.label
    pth = args.path

    dic_init_param = {}
    if args.cmd == "HV ON/OFF":
        dic_init_param["HV ON/OFF"] = True
    elif args.cmd == "V target":
        dic_init_param["V target"] = 3000

    pump_handler = pyipcmini.UsbPumpHandler(serial_port=port, baudrate=baud, init_param=dic_init_param, label=lbl)

    time.sleep(0.01)

    pump_measured_pressure = pump_handler.ion_pump.read_functions.read_pressure()
    pump_measured_current = pump_handler.ion_pump.read_functions.read_current_measured()

    if args.show:
        msg = f"Pressure is {pump_measured_pressure:.2E} mBar and current {pump_measured_current:.2E} A.\n"
        sys.stdout.write(msg)
    else:
        save_measured_values(pressure=pump_measured_pressure, current=pump_measured_current, path=pth)

    pump_handler.close()


##########################################################################################
##########################################################################################
##########################################################################################
# Direct case
##########################################################################################

if __name__ == "__main__":
    main()
