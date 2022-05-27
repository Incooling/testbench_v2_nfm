import setup
from setup import *

rm = pyvisa.ResourceManager()
DAQM907A = rm.open_resource(DAQM970A)
#
DAQM907A.timeout = None  # set a delay
DAQM907A.write("*CLS")  # clear
DAQM907A.write("*RST")  # reset

KEY_34461A = rm.open_resource(setup.KEY_34461A)

KEY_34461A.timeout = None  # set a delay
KEY_34461A.write("*CLS")  # clear
KEY_34461A.write("*RST")  # reset


def setHVAC(voltage):

    DAQM907A.write("SOURce:VOLT " + str(voltage) + ", (@205)\n")

    return voltage


def getHeatVolt():
    KEY_34461A.write(f" MEASure:VOLTage:AC? MAX ,MIN")
    voltage = float(KEY_34461A.read())  # voltage

    return voltage


def getHeatAmp():
    KEY_34461A.write(f" MEASure:CURRent:AC? MAX, MIN")
    current = float(KEY_34461A.read())  # current

    return current
