##########################################################################################
#
# Class for all functions of Agilent IPCMini ion pump controller.
#
##########################################################################################
"""Class for all functions of Agilent IPCMini controller."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .ion_pump_read_functions import PumpReadFunctions
from .ion_pump_set_functions import PumpSetFunctions

if TYPE_CHECKING:
    import serial


class IonPump:
    """Class for all functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize IonPump.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("IonPump")
        self.logger.debug("__init__")

        self.read_functions = PumpReadFunctions(serial_connection)
        self.set_functions = PumpSetFunctions(serial_connection)

    def list_read_function_labels(self) -> int:
        """List all read function labels available.

        Parameters
        ----------
        int
            The list of available read functions keys.

        """
        self.logger.debug("list_read_function_labels")

        return self.read_functions.dic_read_functions.keys()

    def list_set_function_labels(self) -> int:
        """List all set function labels available.

        Parameters
        ----------
        int
            The list of available set functions keys.

        """
        self.logger.debug("list_set_function_labels")

        return self.set_functions.dic_set_functions.keys()


##########################################################################################
##########################################################################################
##########################################################################################
# Direct case
##########################################################################################

if __name__ == "__main__":
    import serial

    logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")
    logger_main = logging.getLogger("__main__")

    PORT = "/dev/ttyUSB0"
    BAUD = 9600
    serial_conn = serial.Serial(port=PORT, baudrate=BAUD, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    serial_conn.timeout = 1
    serial_conn.flushInput()

    pump = IonPump(serial_connection=serial_conn)
    measured_pressure = pump.read_functions.read_pressure()
    measured_current = pump.read_functions.read_current_measured()
    logger_main.debug("Pressure is %.2E mBar and current %.2E A.", measured_pressure, measured_current)

    serial_conn.close()
