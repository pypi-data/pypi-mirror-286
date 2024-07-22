##########################################################################################
#
# Class for general send/receive data functions of Agilent IPCMini ion pump controller.
#
##########################################################################################
"""Class for general send/receive data functions of Agilent IPCMini controller."""

from __future__ import annotations

import logging
from time import sleep
from typing import TYPE_CHECKING

from .ion_pump_dic import IonPumpDics

if TYPE_CHECKING:
    import serial


class PumpBaseFunctions:
    """Class for general send/receive data functions of Agilent IPCMini controller."""

    WAIT_TIME_READ_SERIAL = 0.5  # give the device time to answer via serial (in s)

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpReadFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP base")
        self.logger.debug("__init__")

        self.serial_connection = serial_connection

    def send_read_request(self, request: str) -> bytes:
        """Send read request from IonPumpDics.dics["Win"].

        Parameters
        ----------
        request : str
            The request to send to the controller.

        Returns
        -------
        bytes
            The controller's answer.

        """
        self.logger.debug("send_read_request")
        stx = "02"
        addr = "80"  # Not handled in RS232, 0x80 as placeholder
        if request in IonPumpDics.dics["Win"]:
            win_formatted = IonPumpDics.dics["Win"][request]
            win_formatted = win_formatted.encode("unicode-escape")
            win_formatted = [hex(x).split("x")[-1] for x in win_formatted]
            win = " "
            for win_str in win_formatted:
                win = win + win_str + " "
        else:
            self.logger.debug("Bad request")
            return None
        com = "30"  # 0x30 for read, 0x31 for write
        etx = "03"  # end of transmission
        crc = self.make_crc(base_msg=(addr, win_formatted, com, etx))

        message = bytes.fromhex(stx + " " + addr + win + com + " " + etx + " " + crc[0] + " " + crc[1])
        return self.send_data(message)

    def send_set_request(self, request: str, data_to_set: str) -> bytes:
        """Send set request from IonPumpDics.dics["Win"].

        Parameters
        ----------
        request : str
            The request to send to the controller.
        data_to_set : str
            The data to send to the controller for this request.

        Returns
        -------
        bytes
            The controller's answer.

        """
        self.logger.debug("send_set_request")
        stx = "02"
        addr = "80"  # Not handled in RS232, 0x80 as placeholder
        if request in IonPumpDics.dics["Win"]:
            win_formatted = IonPumpDics.dics["Win"][request]
            win_formatted = win_formatted.encode("unicode-escape")
            win_formatted = [hex(x).split("x")[-1] for x in win_formatted]
            win = " "
            for win_str in win_formatted:
                win = win + win_str + " "
        else:
            self.logger.debug("Bad request")
            return None
        com = "31"  # 0x30 for read, 0x31 for write
        data_formatted = data_to_set.encode("unicode-escape")
        data_formatted = [hex(x).split("x")[-1] for x in data_formatted]
        data = " "
        for byte_str in data_formatted:
            data = data + byte_str + " "
        etx = "03"  # end of transmission
        crc = self.make_crc(base_msg=(addr, win_formatted, com, etx), data=data_formatted)

        message = bytes.fromhex(stx + " " + addr + win + com + data + etx + " " + crc[0] + " " + crc[1])
        return self.send_data(message)

    def make_crc(self, base_msg: tuple[str, str, str, str], *, data: str | None = None) -> list[str]:
        """Make formatted crc message.

        Parameters
        ----------
        base_msg : tuple[str, str, str, str]
            Base part of the message to send to the controller.
        data : str | None
            Data send for a set command, None for a read command.

        Returns
        -------
        list[str]
            The controller's answer.

        """
        self.logger.debug("make_crc")

        (addr, win, com, etx) = base_msg

        win_aux = int(win[0], 16)
        for win_ele in win[1:]:
            win_aux = win_aux ^ int(win_ele, 16)
        if data is None:
            crc = int(addr, 16) ^ win_aux ^ int(com, 16) ^ int(etx, 16)
        else:
            data_aux = int(data[0], 16)
            if len(data) > 1:
                for data_ele in data[1:]:
                    data_aux = data_aux ^ int(data_ele, 16)
            crc = int(addr, 16) ^ win_aux ^ int(com, 16) ^ data_aux ^ int(etx, 16)

        crc = hex(crc)
        crc = crc[2:]
        crc = crc.encode("unicode-escape")
        return [hex(x).split("x")[-1] for x in crc]

    def send_data(self, message: bytes) -> bytes:
        """Send data on serial port and read answer.

        Parameters
        ----------
        message : bytes
            Message to send to the controller.

        Returns
        -------
        bytes
            The controller's answer.

        """
        self.logger.debug("send_data")
        if self.serial_connection.isOpen():
            self.serial_connection.reset_output_buffer()
            self.serial_connection.reset_input_buffer()
            if message:
                msg = "sending message: " + " ".join(hex(n) for n in message)
                self.logger.debug(msg)
                self.serial_connection.write(message)
                self.serial_connection.flush()  # it is buffering. required to get the data out *now*
                return self.read_data()
        return None

    def read_data(self) -> bytes:
        """Read data on serial port.

        Returns
        -------
        bytes
            The controller's answer.

        """
        self.logger.debug("read_data")
        answer = None
        sleep(self.WAIT_TIME_READ_SERIAL)  # give the device time to answer
        if self.serial_connection.inWaiting() > 0:
            self.logger.debug("data present")
            answer = self.serial_connection.read(self.serial_connection.inWaiting())
            msg = "received message: " + " ".join(hex(n) for n in answer)
            self.logger.debug(msg)
        return answer

    def get_reply_after_set_cmd(self, answer: bytes) -> str:
        """Check the status of the answer.

        Parameters
        ----------
        answer : bytes
            The answer from the controller to be assessed.

        Returns
        -------
        str
            Success/fail answer.

        """
        self.logger.debug("get_reply_after_set_cmd")
        result_str = ""
        if answer is not None:
            result_int = hex(answer[2:-3][0])
            result_int = int(result_int[2:])
            result_str = IonPumpDics.dics["Reply"][result_int] if result_int in IonPumpDics.dics["Reply"] else "Unknown reply: " + str(result_int)

        return result_str
