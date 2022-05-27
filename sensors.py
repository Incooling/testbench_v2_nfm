import setup
import pyvisa
import asyncio
import re
from omega_tx import Barometer

heatLoad = list()

rm = pyvisa.ResourceManager()
DAQM901A = rm.open_resource(setup.DAQM970A)

DAQM901A.timeout = None  # set a delay
DAQM901A.write("*CLS")  # clear
DAQM901A.write("*RST")  # reset



def getTemp(channel):
    DAQM901A.write(f"MEAS:TEMP:RTD? 1000,(@{channel})")
    temp = float(DAQM901A.read())

    return temp

def getPressure(channel):
    DAQM901A.write(f" MEASure:VOLTage:DC? (@{channel})")
    value = float(DAQM901A.read())

    pressure = round(8.75 * value - 9.75, 2)

    return pressure  # bar


def getFrequency(channel):
    DAQM901A.write(f"MEAS:FREQ? (@{channel})")
    frequency = float(DAQM901A.read())

    return frequency


def getTempLoad(channel):
    DAQM901A.write(f"MEAS:TEMP:TCouple? K,(@{channel})")
    temp = float(DAQM901A.read())

    return temp


async def read_once():
    async with Barometer('10.58.32.248', '2000') as tx:
        value = str(await tx.get())
        value = re.sub('\D', '', value)
        value = float(value)
        return float(value/10)



