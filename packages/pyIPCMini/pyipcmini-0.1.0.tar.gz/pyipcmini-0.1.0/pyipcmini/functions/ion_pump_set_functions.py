##########################################################################################
#
# Class for set functions of Agilent IPCMini ion pump controller.
#
##########################################################################################
"""Class for set functions of Agilent IPCMini controller."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .ion_pump_base_functions import PumpBaseFunctions
from .ion_pump_dic import IonPumpDic, IonPumpMinMaxDics

if TYPE_CHECKING:
    import serial

##########################################################################################
# All set serial functions
##########################################################################################


class PumpSetSerialFunctions(PumpBaseFunctions):
    """Class for serial set functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpSetSerialFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP set serial")
        self.logger.debug("__init__")

        super().__init__(serial_connection)

    def set_baud_rate(self, baudrate: int) -> str:
        """Set serial baud rate.

        Parameters
        ----------
        baudrate : int
            Baud rate [1=1200 ; 2=2400 ; 3=4800 ; 4=9600].

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_baud_rate")
        if IonPumpMinMaxDics.dic_min_values["BAUDRATE"] <= baudrate <= IonPumpMinMaxDics.dic_max_values["BAUDRATE"]:
            data = str(baudrate)
        else:
            return "Wrong baud rate (1-4)"
        answer = self.send_set_request("Baud rate", data)

        return self.get_reply_after_set_cmd(answer)

    def set_rs485_address(self, address: int = 1) -> str:
        """Set RS485 serial address.

        Parameters
        ----------
        address : int
            RS485 address [0-31] (1=def).

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_rs485_address")
        if IonPumpMinMaxDics.dic_min_values["ADDRESS"] <= address <= IonPumpMinMaxDics.dic_max_values["ADDRESS"]:
            data = str(address)
        else:
            return "Address out of range (0-31)"
        answer = self.send_set_request("RS485 address", data)

        return self.get_reply_after_set_cmd(answer)

    def set_serial_type(self, serial_type: int = 0) -> str:
        """Set serial type.

        Parameters
        ----------
        serial_type : int
            Serial type [0 = RS232 (def) ; 1 = RS485].

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_serial_type")
        if 0 <= serial_type <= 1:
            data = str(serial_type)
        else:
            return "Wrong serial type (0-1)"
        answer = self.send_set_request("Serial type", data)

        return self.get_reply_after_set_cmd(answer)


##########################################################################################
# All set ID functions
##########################################################################################


class PumpSetIdFunctions(PumpBaseFunctions):
    """Class for ID set functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpSetIdFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP set ID")
        self.logger.debug("__init__")

        super().__init__(serial_connection)

    def set_device_number(self, number: int) -> str:
        """Set device number.

        Parameters
        ----------
        number : int
            Depending on the pump type, see parent_pump.dic_device_number.

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_device_number")
        if number in IonPumpDic.dic_device_number:
            data = str(number)
        else:
            return "Wrong device number"
        answer = self.send_set_request("Device number", data)

        return self.get_reply_after_set_cmd(answer)

    def set_label(self, label: str) -> str:
        """Set device label.

        Parameters
        ----------
        label : str
            Max 10 characters.

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_label")
        if len(label) > IonPumpMinMaxDics.dic_max_values["LABEL_LENGTH"]:
            return "Label too long"
        data = label
        answer = self.send_set_request("Label", data)

        return self.get_reply_after_set_cmd(answer)


##########################################################################################
# All set functions
##########################################################################################


class PumpSetFunctions(PumpSetSerialFunctions, PumpSetIdFunctions):
    """Class for read functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpSetFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP set")
        self.logger.debug("__init__")

        super().__init__(serial_connection)

        self.dic_set_functions = {
            "Mode": self.set_mode,
            "HV ON/OFF": lambda x: self.set_hv_on_off(on_off=x),
            "Baud rate": self.set_baud_rate,
            "RS485 address": self.set_rs485_address,
            "Serial type": self.set_serial_type,
            "Unit pressure": self.set_unit_pressure,
            "Autostart": lambda x: self.set_autostart(on_off=x),
            "Protect": lambda x: self.set_protect(on_off=x),
            "Fixed/step": lambda x: self.set_fixed_step(on_off=x),
            "Device number": self.set_device_number,
            "Max power": self.set_max_power,
            "V target": self.set_voltage_target,
            "I protect": self.set_current_protect,
            "Set point": self.set_setpoint,
            "Label": self.set_label,
        }

    def set_mode(self, mode: int) -> str:
        """Set the communication mode.

        Parameters
        ----------
        mode : int
            [0=Serial ; 1=Remote ; 2=Local ; 3=LAN], see parent_pump.dic_mode.

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_mode")
        if IonPumpMinMaxDics.dic_min_values["MODE"] <= mode <= IonPumpMinMaxDics.dic_max_values["MODE"]:
            data = str(mode)
        else:
            return "Wrong mode (0-3)"
        data = str(int(mode))
        answer = self.send_set_request("Mode", data)

        return self.get_reply_after_set_cmd(answer)

    def set_hv_on_off(self, *, on_off: bool) -> str:
        """Set HV output ON/OFF.

        Parameters
        ----------
        on_off : bool
            [0=OFF ; 1=ON].

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_hv_on_off")
        data = str(int(on_off))
        answer = self.send_set_request("HV ON/OFF", data)

        return self.get_reply_after_set_cmd(answer)

    def set_unit_pressure(self, unit: int) -> str:
        """Set unit pressure.

        Parameters
        ----------
        unit : int
            [0=Torr ; 1=mBar ; 2=Pa], see parent_pump.dic_pressure_unit.

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_unit_pressure")
        if IonPumpMinMaxDics.dic_min_values["UNIT_PRESSURE"] <= unit <= IonPumpMinMaxDics.dic_max_values["UNIT_PRESSURE"]:
            data = str(unit)
        else:
            return "Wrong unit (0-2)"
        answer = self.send_set_request("Unit pressure", data)

        return self.get_reply_after_set_cmd(answer)

    def set_autostart(self, *, on_off: bool) -> str:
        """Set autostart.

        Parameters
        ----------
        on_off : bool
            [0=disabled ; 1=enabled].

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_autostart")
        data = str(int(on_off))
        answer = self.send_set_request("Autostart", data)

        return self.get_reply_after_set_cmd(answer)

    def set_protect(self, *, on_off: bool) -> str:
        """Set protect current.

        Parameters
        ----------
        on_off : bool
            [0=disabled ; 1=enabled].

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_protect")
        data = str(int(on_off))
        answer = self.send_set_request("Protect", data)

        return self.get_reply_after_set_cmd(answer)

    def set_fixed_step(self, *, on_off: bool) -> str:
        """Set fixed/step status.

        Parameters
        ----------
        on_off : bool
            [0=disabled ; 1=enabled].

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_fixed_step")
        data = str(int(on_off))
        answer = self.send_set_request("Fixed/step", data)

        return self.get_reply_after_set_cmd(answer)

    def set_max_power(self, power: int) -> str:
        """Set max power.

        Parameters
        ----------
        power : int
            [10-40]  (in W).

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_max_power")
        if IonPumpMinMaxDics.dic_min_values["POWER"] <= power <= IonPumpMinMaxDics.dic_max_values["POWER"]:
            data = str(power)
        else:
            return "Max power out of range (10-40)"
        answer = self.send_set_request("Max power", data)

        return self.get_reply_after_set_cmd(answer)

    def set_voltage_target(self, voltage: int) -> str:
        """Set target voltage.

        Parameters
        ----------
        voltage : int
            [3000-7000]  (in V).

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_voltage_target")
        if IonPumpMinMaxDics.dic_min_values["VOLTAGE"] <= voltage <= IonPumpMinMaxDics.dic_max_values["VOLTAGE"]:
            data = str(voltage)
        else:
            return "Voltage out of range (3000-7000)"
        answer = self.send_set_request("V target", data)

        return self.get_reply_after_set_cmd(answer)

    def set_current_protect(self, current: int) -> str:
        """Set protect current.

        Parameters
        ----------
        current : int
            [1-10000] (in microA)..

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_current_protect")
        if IonPumpMinMaxDics.dic_min_values["PROTECT_CURRENT"] <= current <= IonPumpMinMaxDics.dic_max_values["PROTECT_CURRENT"]:
            data = str(current)
        else:
            return "Current out of range (1-10000)"
        answer = self.send_set_request("I protect", data)

        return self.get_reply_after_set_cmd(answer)

    def set_setpoint(self, setpoint_current: float) -> str:
        """Set the set point current.

        Parameters
        ----------
        setpoint_current : float
            X.XE-XX [1.0E-10 - 1.0E-5] (in A).

        Returns
        -------
        str
            Pump reply.

        """
        self.logger.debug("set_setpoint")
        if IonPumpMinMaxDics.dic_min_values["SETPOINT_CURRENT"] <= setpoint_current <= IonPumpMinMaxDics.dic_max_values["SETPOINT_CURRENT"]:
            data = f"{setpoint_current:.1E}"
        else:
            return "Set point out of range (1.0E-10 - 1.0E-5)"
        answer = self.send_set_request("Set point", data)

        return self.get_reply_after_set_cmd(answer)
