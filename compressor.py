from time import sleep

import pyvisa
from setup import *
import re

# Setup connection
rm = pyvisa.ResourceManager()
QPX1200SP_1 = rm.open_resource(QPX1200SP_1)

# Power supply 1
QPX1200SP_1.timeout = 10000  # set a delay
QPX1200SP_1.read_termination = '\r'

DAQM970A = rm.open_resource(DAQM970A)
#
DAQM970A.clear()
DAQM970A.timeout = 10000  # set a delay
DAQM970A.write("*CLS")  # clear
DAQM970A.write("*RST")  # reset

rm.list_resources()
('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
scope = rm.open_resource(MDO3024)

scope.timeout = 10000  # ms
scope.write("*CLS")  # clear
scope.write("*RST")  # reset
scope.encoding = 'latin_1'
scope.read_termination = '\n'
scope.write_termination = None

scope.write("MEASUREMENT:MEAS1:STATE ON")
scope.write('MEASUREMENT:MEAS1:SOURCE1')
scope.write("MEASUREMENT:MEAS1:TYPE FREQUENCY")

scope.write("MEASUREMENT:MEAS2:STATE ON")
scope.write('MEASUREMENT:MEAS2:SOURCE1')
scope.write("MEASUREMENT:MEAS2:TYPE FREQUENCY")

scope.write("MEASUREMENT:MEAS3:STATE ON")
scope.write('MEASUREMENT:MEAS3:SOURCE1')
scope.write("MEASUREMENT:MEAS3:TYPE FREQUENCY")

scope.write("MEASUREMENT:MEAS4:STATE ON")
scope.write('MEASUREMENT:MEAS4:SOURCE1')
scope.write("MEASUREMENT:MEAS4:TYPE FREQUENCY")

scope.write('CH1:SCALE 5E0')
scope.write('HORIZONTAL:SCALE 4E-03')

scope.write("CH1:PRObe:DEGAUss EXECute")


def getFFT():
    q_str = scope.query("MATH:DEFINE \"FFT(CH1)\"")
    return q_str


def get_comp_freq():
    q_str = scope.query("MEASUREMENT:MEAS1:VALUE?")
    return q_str
#
#
# def getMaxCompSpeed():
#     q_str = scope.query("MEASUREMENT:MEAS2:MAXimum?")
#     return q_str
#
#
# def getMinCompSpeed():
#     q_str = scope.query("MEASUREMENT:MEAS3:MINimum?")
#     return q_str
#
#
# def getAvgCompSpeed():
#     q_str = scope.query("MEASUREMENT:MEAS4:MEAN?")
#
#     return q_str


def getCurrentSupply():
    QPX1200SP_1.write(f"I1O?\r")
    current = QPX1200SP_1.read()
    current = re.sub('\D', '', current)

    return float(current)


def getVoltageSupply():
    QPX1200SP_1.write(f"V1O?\r")
    voltage = QPX1200SP_1.read()
    voltage = re.sub('\D', '', voltage)

    return float(voltage)


def setCompressor(voltage):
    DAQM970A.write("SOURce:VOLT " + str(voltage) + ", (@204)")

    return voltage


def setQPX1200SP_1(voltage, state):
    QPX1200SP_1.write(f"V1 {voltage}\r")
    QPX1200SP_1.write(f"OP1 {state}\r")


def getCurrentComp():
    DAQM970A.write("MEASure:VOLTage:DC? (@112)")

    current = float((DAQM970A.read()))

    return current


def getStatus():
    DAQM970A.write(" DIG:DATA:BYTE? (@201)")
    status = float((DAQM970A.read()))
    status = int(status)
    status = (status & 0x01) >> 0

    if status == 0:
        status = "normal"
    else:
        status = "warning"

    return str(status)


def getOverheat():
    DAQM970A.write(" DIG:DATA:BYTE? (@201)")
    overheat = float((DAQM970A.read()))
    overheat = int(overheat)
    overheat = (overheat & 0x02) >> 1

    if overheat == 0:
        overheat = "normal"
    else:
        overheat = "overheat"

    return str(overheat)


def setEnable(state):
    if state:
        DAQM970A.write("SOURce:DIG:DATA #b00000000, (@202)")
    elif not state:
        DAQM970A.write("SOURce:DIG:DATA #b00000001, (@202)")

    return state


def refresh_scope():
    scope.write("MEASUREMENT:MEAS1:STATE OFF")
    scope.write("MEASUREMENT:MEAS2:STATE OFF")
    scope.write("MEASUREMENT:MEAS3:STATE OFF")
    scope.write("MEASUREMENT:MEAS4:STATE OFF")

    scope.write("MEASUREMENT:MEAS1:STATE ON")
    scope.write("MEASUREMENT:MEAS2:STATE ON")
    scope.write("MEASUREMENT:MEAS3:STATE ON")
    scope.write("MEASUREMENT:MEAS4:STATE ON")
