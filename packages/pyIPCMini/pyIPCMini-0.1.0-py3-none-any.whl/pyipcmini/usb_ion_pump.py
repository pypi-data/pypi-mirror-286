##########################################################################################
#
# Class to communicate with an Agilent IPCMini ion pump controller via RS232 serial.
#
# Tested on standard USB port of raspberry pi 4 with FTDI USB/serial converter.
#
##########################################################################################
"""Contain the class for Agilent IPCMini controller."""

from __future__ import annotations

import dataclasses
import logging
import threading
import time
from datetime import datetime as dt
from queue import Queue

import serial
from dateutil import tz

from .functions import IonPump, IonPumpDics


@dataclasses.dataclass
class MeasureTimes:
    """Times used to timestamp measurements."""

    time: float
    time_stamp: dt
    old_time: float


class CustomError(Exception):
    """Custom error class."""


##########################################################################################
# Class for addressing the Agilent IPCMini controller.
##########################################################################################


class UsbPumpHandler:
    """Class for addressing the Agilent IPCMini controller."""

    TIME_ZONE = tz.gettz("Europe / Paris")

    ##########################################################################################
    # Init / close functions
    ##########################################################################################

    def __init__(self, serial_port: str = "/dev/ttyUSB0", baudrate: int = 9600, init_param: dict | None = None, label: str = "Label") -> None:
        """Initialise the UsbPumpHandler.

        Parameters
        ----------
        serial_port : str
            On which COM port your pump controller is connected to.
        baudrate : int
            Value of the baudrate for COM port. By default 9600 on IPCMini.
        init_param : dict
            All parameters of the pump controller to be initialized.
        label : str
            Pump driver label, to check whether this is the correct pump.

        Raises
        ------
        CustomError
            Wrong pump name.

        """
        self.logger = logging.getLogger("USB PUMP serial - " + serial_port)
        self.logger.debug("__init__")

        self.thread_killed = False  # Set to true to kill a running thread for this object

        self.timings = MeasureTimes(time=time.time(), time_stamp=dt.now(tz=UsbPumpHandler.TIME_ZONE), old_time=time.time())

        self.serial_connection = serial.Serial(port=serial_port, baudrate=baudrate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        self.serial_connection.timeout = 1
        self.serial_connection.flushInput()

        self.ion_pump = IonPump(self.serial_connection)

        if init_param is not None:
            if self.ion_pump.read_functions.read_label() != label:
                msg = "Wrong pump (inverted USB ports?)"
                raise CustomError(msg)
            self.initialize_parameters(init_param)

    def initialize_parameters(self, init_param: dict) -> None:
        """Initialize standard parameters.

        Parameters
        ----------
        init_param : dict
            All parameters of the pump controller to be initialized.

        """
        self.logger.debug("initialize_parameters")
        for param in init_param:
            answer = self.ion_pump.read_functions.dic_read_functions[param]()

            if param in IonPumpDics.dics:
                already_set = answer == IonPumpDics.dics[param][init_param[param]] if init_param[param] in IonPumpDics.dics[param] else False
            else:
                already_set = answer == init_param[param]

            if not already_set:
                self.logger.debug("INITIALIZING: %s", param)
                acknowledgement = self.ion_pump.set_functions.dic_set_functions[param](init_param[param])
                msg = "INITIALIZING: " + param + " gives " + acknowledgement
                self.logger.debug(msg)
            else:
                self.logger.debug("INITIALIZING: %s already set", param)

    def close(self) -> None:
        """Close the serial connection, free up the COM port."""
        self.logger.debug("close")
        self.serial_connection.close()

    ##########################################################################################
    # Loop function to be called by a thread
    ##########################################################################################

    def thread_loop(self, values_queue: Queue, commands_queue: Queue, update_values_time: float = 30.0, update_commands_time: float = 2.0) -> None:
        """Loop thread for pressure and temperature.

        Loops reading the pressure and current every update_time,
        then sends them via the thread's value Queue, along with a time stamp.

        Parameters
        ----------
        values_queue : Queue
            To pass data collected within a thread to the app that started the thread.
        commands_queue : Queue
            To send commands while thread is running.
        update_values_time : float
            Time interval between measurements
            => in principle, should be longer than update_commands_time.
        update_commands_time : float
            Time interval between checks for commands.

        """
        self.logger.debug("thread_loop")

        self.timings.old_time = time.time()

        while True:
            while commands_queue.qsize() > 0:
                command_type, command_value = commands_queue.get()
                self.ion_pump.set_functions.dic_set_functions[command_type](command_value)

            time.sleep(update_commands_time)

            self.timings.time = time.time()
            if (self.timings.time - self.timings.old_time) > update_values_time:
                self.timings.old_time = self.timings.time

                self.timings.time_stamp = dt.now(tz=UsbPumpHandler.TIME_ZONE)
                measured_pressure = self.ion_pump.read_functions.read_pressure()
                measured_current = self.ion_pump.read_functions.read_current_measured()
                values_queue.put([measured_pressure, measured_current, self.timings.time_stamp])

            if self.thread_killed:
                self.thread_killed = False
                break

    def kill_thread(self) -> None:
        """Kill the thread."""
        self.logger.debug("kill_thread")

        self.thread_killed = True


##########################################################################################
##########################################################################################
##########################################################################################
# Direct case
##########################################################################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")
    logger_main = logging.getLogger("__main__")

    dic_init_param = {
        "Protect": True,
        "Fixed/step": False,
        "Autostart": True,
        "Max power": 40,
        "I protect": 5000,
        "Set point": 1e-08,
        "Label": "Sr Oven",
        "Unit pressure": 1,
        "Device number": 5,
        "V target": 5000,
        "HV ON/OFF": True,
    }

    PORT = "/dev/ttyUSB0"
    BAUD = 9600
    serial_conn = UsbPumpHandler(serial_port=PORT, baudrate=BAUD, init_param=dic_init_param, label="Sr Oven")

    UPDATE_TIME = 15.0  # in seconds
    pump_readings_values_queue = Queue()
    pump_commands_values_queue = Queue()
    thread = threading.Thread(target=serial_conn.thread_loop, args=(pump_readings_values_queue, pump_commands_values_queue, UPDATE_TIME), daemon=True)
    thread.start()

    try:
        LOOP_BOOL = True
        while LOOP_BOOL:
            if pump_readings_values_queue.qsize() > 0:
                pump_measured_pressure, pump_measured_current, pump_measurement_time = pump_readings_values_queue.get()
                logger_main.debug("Measurement at time:")
                logger_main.debug("%f", pump_measurement_time)
                logger_main.debug("Pressure is %.2E mBar and current %.2E A.", pump_measured_pressure, pump_measured_current)

            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        logger_main.debug(" ")
        logger_main.debug("Program interrupted by user (ctrl+C)")

    serial_conn.kill_thread()
    thread.join()
    if not thread.is_alive():
        logger_main.debug("Thread killed")

    serial_conn.close()
