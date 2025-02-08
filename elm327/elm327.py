import bluetooth
import argparse
import re

ELM327_CMD_WARM_START = "AT WS"
ELM327_CMD_VERSION = "AT I"
ELM327_CMD_READ_VOLTAGE = "AT RV"
ELM327_CMD_CALIBRATE_VOLTAGE = "AT CV"
OBD_CMD_READ_STORED_DTC = "03"
OBD_CMD_READ_PENDING_DTC = "07"
OBD_CMD_CLEAR = "04"

class AdapterException(Exception):
    pass

class Adapter():

    def __init__(self, address):
        self.address = address
        self.socket = None

    def get_address(self):
        return self.address

    def connect(self):
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((self.address, 1))
        socket.setblocking(False)
        self.socket = socket
        return socket

    def disconnect(self):
        self.socket.close()

    def write(self, data):
        self.socket.send(f'{data}\r')

    def read(self):
        buffer = b""
        while True:
            try:
                byte = self.socket.recv(1)
                if byte == b">":
                    break
                else:
                    buffer += byte
            except:
                pass
        return buffer

    def reset(self):
        self.write(ELM327_CMD_WARM_START)
        response = self.read()

        response_pattern = re.compile("AT WS\\r\\r\\rELM327 v[0-9.]*\\r\\r")

        if not response_pattern.match(response.decode()):
            raise AdapterException("Adapter error occured!")

    def read_version(self):
        self.write(ELM327_CMD_VERSION)
        response = self.read()

        response_pattern = re.compile("AT I\\rELM327 v[0-9.]*\\r\\r")
        if not response_pattern.match(response.decode()):
            raise AdapterException("Addapter error occured!")

        version_pattern = re.compile("v[0-9.]*")
        response_version = version_pattern.search(response.decode()).group(0)

        return response_version


    def read_voltage(self):
        self.write(ELM327_CMD_READ_VOLTAGE)
        response = self.read()

        response_pattern = re.compile("AT RV\\r[0-9]{1,2}[.][0-9]{1,2}V\\r\\r")
        if not response_pattern.match(response.decode()):
            raise AdapterException("Adapter error occured!")

        voltage_pattern = re.compile("[0-9]{1,2}[.][0-9]{1,2}V")
        response_voltage = voltage_pattern.search(response.decode()).group(0)

        return int(float(response_voltage[:-1]) * 100)

    def calibrate_voltage(self, voltage):
        voltage = int(voltage * 100)

        self.write(f"{ELM327_CMD_CALIBRATE_VOLTAGE} {voltage}")
        response = self.read()

        response_pattern = re.compile("AT CV [0-9]{1,4}\\rOK\\r\\r")
        if not response_pattern.match(response.decode()):
            raise AdapterException("Adapter error occured!")

    def read_dtc(self):
        self.write(OBD_CMD_READ_STORED_DTC)
        response = self.read()

        bus_error_pattern = re.compile("03\\rCAN ERROR\\r\\r")
        if bus_error_pattern.match(response.decode()):
            raise AdapterException("CAN bus error occured!")

        print(response)

    def read_pending_dtc(self):
        self.write(OBD_CMD_READ_PENDING_DTC)
        response = self.read()

        bus_error_pattern = re.compile("07\\rCAN ERROR\\r\\r")
        if bus_error_pattern.match(response.decode()):
            raise AdapterException("CAN bus error occured!")

        print(response)

    def clear(self):
        self.write(OBD_CMD_CLEAR)
        response = self.read()

        bus_error_pattern = re.compile("04\\rCAN ERROR\\r\\r")
        if bus_error_pattern.match(response.decode()):
            raise AdapterException("CAN bus error occured!")

        print(response)

