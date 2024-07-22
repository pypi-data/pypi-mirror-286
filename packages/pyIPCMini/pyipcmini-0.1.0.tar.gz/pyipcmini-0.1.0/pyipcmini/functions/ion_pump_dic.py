##########################################################################################
#
# Class of dictionnaries for Agilent IPCMini ion pump controller.
#
##########################################################################################
"""Contain the class of dictionnaries for Agilent IPCMini ion pump controller."""

import dataclasses
from types import MappingProxyType


@dataclasses.dataclass
class IonPumpDic:
    """Class of dictionnaries for Agilent IPCMini ion pump controller."""

    dic_reply = MappingProxyType({6: "Command success", 15: "Command fail", 32: "Invalid window", 33: "Data type error", 34: "Out of range", 35: "Window is read-only"})
    dic_mode = MappingProxyType({0: "Serial", 1: "Remote", 2: "Local", 3: "LAN"})
    dic_baud_rate = MappingProxyType({1: 1200, 2: 2400, 3: 4800, 4: 9600})
    dic_serial_type = MappingProxyType({False: "RS232", True: "RS485"})
    dic_pressure_unit = MappingProxyType({0: "Torr", 1: "mBar", 2: "Pa"})

    dic_device_number = MappingProxyType(
        {
            0: "Spare",
            1: "500 StarCell",
            2: "300 StarCell",
            16: "200 StarCell",
            3: "150 StarCell",
            4: "75-55-40 StarCell",
            5: "20 StarCell",
            20: "NEXTorr-SC",
            6: "500 diode",
            7: "300 diode",
            15: "200 diode",
            8: "150 diode",
            9: "75-55-40 diode",
            10: "20 diode",
            11: "10 diode",
            12: "75 Sem",
            13: "75 Sem",
            14: "75 Sem",
            17: "2 diode",
            18: "0.2 diode 1250 Gauss",
            19: "0.2 diode 800 Gauss",
        },
    )

    dic_win = MappingProxyType(
        {
            "Mode": "008",
            "HV ON/OFF": "011",
            "Baud rate": "108",
            "Status": "205",
            "Error code": "206",
            "Model": "319",
            "Serial number": "323",
            "RS485 address": "503",
            "Serial type": "504",
            "Unit pressure": "600",
            "Autostart": "601",
            "Protect": "602",
            "Fixed/step": "603",
            "Device number": "610",
            "Max power": "612",
            "V target": "613",
            "I protect": "614",
            "Set point": "615",
            "Temperature power section": "800",
            "Temperature internal controller": "801",
            "Status set point": "804",
            "V measured": "810",
            "I measured": "811",
            "Pressure": "812",
            "Label": "890",
        },
    )


@dataclasses.dataclass
class IonPumpDics:
    """Class of joint dictionnaries for Agilent IPCMini ion pump controller."""

    dics = MappingProxyType(
        {
            "Reply": IonPumpDic.dic_reply,
            "Mode": IonPumpDic.dic_mode,
            "Baud rate": IonPumpDic.dic_baud_rate,
            "Serial type": IonPumpDic.dic_serial_type,
            "Unit pressure": IonPumpDic.dic_pressure_unit,
            "Device number": IonPumpDic.dic_device_number,
            "Win": IonPumpDic.dic_win,
        },
    )


@dataclasses.dataclass
class IonPumpMinMaxDics:
    """Class of min/max values dictionnaries for Agilent IPCMini ion pump controller."""

    dic_max_values = MappingProxyType(
        {"LABEL_LENGTH": 10, "SETPOINT_CURRENT": 1.0e-5, "PROTECT_CURRENT": 10000, "VOLTAGE": 7000, "POWER": 40, "UNIT_PRESSURE": 2, "ADDRESS": 31, "BAUDRATE": 4, "MODE": 3},
    )

    dic_min_values = MappingProxyType({"SETPOINT_CURRENT": 1.0e-10, "PROTECT_CURRENT": 1, "VOLTAGE": 3000, "POWER": 10, "UNIT_PRESSURE": 0, "ADDRESS": 0, "BAUDRATE": 1, "MODE": 0})
