##########################################################################################
#
# Class for read functions of Agilent IPCMini ion pump controller.
#
##########################################################################################
"""Class for read functions of Agilent IPCMini controller."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .ion_pump_base_functions import PumpBaseFunctions
from .ion_pump_dic import IonPumpDic

if TYPE_CHECKING:
    import serial

##########################################################################################
# All read serial functions
##########################################################################################


class PumpReadSerialFunctions(PumpBaseFunctions):
    """Class for serial read functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpReadSerialFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP read serial")
        self.logger.debug("__init__")

        super().__init__(serial_connection)

    def read_baud_rate(self) -> int:
        """Read serial baud rate.

        Returns
        -------
        int
            Baud rate [1=1200 ; 2=2400 ; 3=4800 ; 4=9600].

        """
        self.logger.debug("read_baud_rate")
        answer = self.send_read_request("Baud rate")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
            result = IonPumpDic.dic_baud_rate[result]
        return result

    def read_rs485_address(self) -> int:
        """Read RS485 serial address.

        Returns
        -------
        int
            Address [0-31].

        """
        self.logger.debug("read_rs485_address")
        answer = self.send_read_request("RS485 address")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_serial_type(self) -> str:
        """Read serial type select.

        Returns
        -------
        str
            Serial type [RS232 ; RS485].

        """
        self.logger.debug("read_serial_type")
        answer = self.send_read_request("Serial type")
        result = ""
        if answer is not None:
            result = bool(int(answer[6:-3].decode("ascii")))
            result = IonPumpDic.dic_serial_type[result]
        return result


##########################################################################################
# All read ID functions
##########################################################################################


class PumpReadIdFunctions(PumpBaseFunctions):
    """Class for ID read functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpReadIdFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP read ID")
        self.logger.debug("__init__")

        super().__init__(serial_connection)

    def read_serial_number(self) -> str:
        """Read device serial number.

        Returns
        -------
        str
            Device serial number.

        """
        self.logger.debug("read_serial_number")
        answer = self.send_read_request("Serial number")
        result = ""
        if answer is not None:
            result = answer[6:-3].decode("ascii")
        return result

    def read_device_number(self) -> str:
        """Read device number.

        Returns
        -------
        str
            Device number giving the pump type, see parent_pump.dic_device_number.

        """
        self.logger.debug("read_device_number")
        answer = self.send_read_request("Device number")
        result = ""
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
            result = IonPumpDic.dic_device_number[result]
        return result

    def read_label(self) -> str:
        """Read device label.

        Returns
        -------
        str
            Device label.

        """
        self.logger.debug("read_label")
        answer = self.send_read_request("Label")
        result = None
        if answer is not None:
            result = answer[6:-3].decode("ascii")
        return result


##########################################################################################
# All read functions
##########################################################################################


class PumpReadFunctions(PumpReadSerialFunctions, PumpReadIdFunctions):
    """Class for read functions of Agilent IPCMini controller."""

    def __init__(self, serial_connection: serial.Serial) -> None:
        """Initialize PumpReadFunctions.

        Parameters
        ----------
        serial_connection : serial.Serial
            The USB serial connection for the IPCMini.

        """
        self.logger = logging.getLogger("PUMP read")
        self.logger.debug("__init__")

        super().__init__(serial_connection)

        self.dic_read_functions = {
            "Mode": self.read_mode,
            "HV ON/OFF": self.read_hv_on_off,
            "Baud rate": self.read_baud_rate,
            "Status": self.read_status,
            "Error code": self.read_error_code,
            "Model": self.read_controller_model,
            "Serial number": self.read_serial_number,
            "RS485 address": self.read_rs485_address,
            "Serial type": self.read_serial_type,
            "Unit pressure": self.read_unit_pressure,
            "Autostart": self.read_autostart,
            "Protect": self.read_protect,
            "Fixed/step": self.read_fixed_step,
            "Device number": self.read_device_number,
            "Max power": self.read_max_power,
            "V target": self.read_voltage_target,
            "I protect": self.read_current_protect,
            "Set point": self.read_setpoint,
            "Temperature power section": self.read_temperature_power_section,
            "Temperature internal controller": self.read_temperature_internal_controller,
            "Status set point": self.read_status_setpoint,
            "V measured": self.read_voltage_measured,
            "I measured": self.read_current_measured,
            "Pressure": self.read_pressure,
            "Label": self.read_label,
        }

    def read_mode(self) -> str:
        """Read the communication mode.

        Returns
        -------
        str
            Mode, see parent_pump.dic_mode.

        """
        self.logger.debug("read_mode")
        answer = self.send_read_request("Mode")
        result = ""
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
            result = IonPumpDic.dic_mode[result]
        return result

    def read_hv_on_off(self) -> bool:
        """Read HV status.

        Returns
        -------
        bool
            HV status [0=OFF ; 1=ON].

        """
        self.logger.debug("read_hv_on_off")
        answer = self.send_read_request("HV ON/OFF")
        result = None
        if answer is not None:
            result = bool(int(answer[6:-3].decode("ascii")))
        return result

    def read_status(self) -> int:
        """Read status.

        Returns
        -------
        int
            Status [0=OK ; 5=HV ON ; 6=Fail].

        """
        self.logger.debug("read_status")
        answer = self.send_read_request("Status")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_error_code(self) -> int:
        """Read error code.

        Returns
        -------
        int
            Error code [0=No error ; 4=Over Temperature ;
                32=Interlock cable ; 64=ShortCircuit ; 128=Protect].

        """
        self.logger.debug("read_error_code")
        answer = self.send_read_request("Error code")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_controller_model(self) -> str:
        """Read controller model.

        Returns
        -------
        str
            Controller model.

        """
        self.logger.debug("read_controller_model")
        answer = self.send_read_request("Model")
        result = ""
        if answer is not None:
            result = answer[6:-3].decode("ascii")
        return result

    def read_unit_pressure(self) -> str:
        """Read unit pressure.

        Returns
        -------
        str
            Unit pressure, see parent_pump.dic_pressure_unit.

        """
        self.logger.debug("read_unit_pressure")
        answer = self.send_read_request("Unit pressure")
        result = ""
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
            result = IonPumpDic.dic_pressure_unit[result]
        return result

    def read_autostart(self) -> bool:
        """Read autostart status.

        Returns
        -------
        bool
            Autostart status [0=disabled ; 1=enabled].

        """
        self.logger.debug("read_autostart")
        answer = self.send_read_request("Autostart")
        result = None
        if answer is not None:
            result = bool(int(answer[6:-3].decode("ascii")))
        return result

    def read_protect(self) -> bool:
        """Read protect status.

        Returns
        -------
        bool
            Protect status [0=disabled ; 1=enabled].

        """
        self.logger.debug("read_protect")
        answer = self.send_read_request("Protect")
        result = None
        if answer is not None:
            result = bool(int(answer[6:-3].decode("ascii")))
        return result

    def read_fixed_step(self) -> bool:
        """Read fixed/step status.

        Returns
        -------
        bool
            Fixed/step status [0=disabled ; 1=enabled].

        """
        self.logger.debug("read_fixed_step")
        answer = self.send_read_request("Fixed/step")
        result = None
        if answer is not None:
            result = bool(int(answer[6:-3].decode("ascii")))
        return result

    def read_max_power(self) -> int:
        """Read max power.

        Returns
        -------
        int
            Power (in W).

        """
        self.logger.debug("read_max_power")
        answer = self.send_read_request("Max power")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_voltage_target(self) -> int:
        """Read target voltage.

        Returns
        -------
        int
            Voltage (in V).

        """
        self.logger.debug("read_voltage_target")
        answer = self.send_read_request("V target")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_current_protect(self) -> int:
        """Read protect current.

        Returns
        -------
        int
            Current (in microA).

        """
        self.logger.debug("read_current_protect")
        answer = self.send_read_request("I protect")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_setpoint(self) -> float:
        """Read set point current.

        Returns
        -------
        float
            Set point (in A).

        """
        self.logger.debug("read_setpoint")
        answer = self.send_read_request("Set point")
        result = None
        if answer is not None:
            result = float(answer[6:-3].decode("ascii"))
        return result

    def read_temperature_power_section(self) -> float:
        """Read temperature of power section.

        Returns
        -------
        float
            Temperature (in degC).

        """
        self.logger.debug("read_temperature_power_section")
        answer = self.send_read_request("Temperature power section")
        result = None
        if answer is not None:
            result = float(answer[6:-3].decode("ascii"))
            result = result / 10.0
        return result

    def read_temperature_internal_controller(self) -> float:
        """Read temperature of internal controller.

        Returns
        -------
        float
            Temperature (in degC).

        """
        self.logger.debug("read_temperature_internal_controller")
        answer = self.send_read_request("Temperature internal controller")
        result = None
        if answer is not None:
            result = float(answer[6:-3].decode("ascii"))
            result = result / 10.0
        return result

    def read_status_setpoint(self) -> bool:
        """Read set point status.

        Returns
        -------
        bool
            Set point status [0=OFF ; 1=ON].

        """
        self.logger.debug("read_status_setpoint")
        answer = self.send_read_request("Status set point")
        result = None
        if answer is not None:
            result = bool(int(answer[6:-3].decode("ascii")))
        return result

    def read_voltage_measured(self) -> int:
        """Read measured voltage.

        Returns
        -------
        int
            Voltage (in V).

        """
        self.logger.debug("read_voltage_measured")
        answer = self.send_read_request("V measured")
        result = None
        if answer is not None:
            result = int(answer[6:-3].decode("ascii"))
        return result

    def read_current_measured(self) -> float:
        """Read measured current.

        Returns
        -------
        float
            Current (in A).

        """
        self.logger.debug("read_current_measured")
        answer = self.send_read_request("I measured")
        result = None
        if answer is not None:
            result = float(answer[6:-3].decode("ascii"))
        return result

    def read_pressure(self) -> float:
        """Read measured pressure.

        Returns
        -------
        float
            Pressure (in pressure unit).

        """
        self.logger.debug("read_pressure")
        answer = self.send_read_request("Pressure")
        result = None
        if answer is not None:
            result = float(answer[6:-3].decode("ascii"))
        return result
