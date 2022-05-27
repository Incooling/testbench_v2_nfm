import compressor
import hvac
import sensors
from MX100QP import ttiPsu
from setup import *
from time import sleep
#
# pressure sensors
ttiPsu.setTargetVolts(2, 12)
ttiPsu.setOutputEnable(2, True)

# Pressure
p_evap_out.append(sensors.getPressure(105))  # pressure 2
p_cond_in.append(sensors.getPressure(106))  # pressure 3
p_flow_out.append(sensors.getPressure(107))  # pressure 4
t_load_middle.append(round(sensors.getTempLoad(109), 1))

print(p_evap_out)
print(p_cond_in)
print(p_flow_out)

t_load_ambient.append(round(sensors.getTempLoad(111), 1))

print(t_load_ambient)
#
ttiPsu.setTargetVolts(1, 12)
ttiPsu.setOutputEnable(1, False)
#
# set_data.insert(0, hvac.setHVAC(0))  # 1.78
compressor.setCompressor(0)
compressor.setQPX1200SP_1(24, 1)
compressor.setEnable(True)
#
# while True:
#     print(t_load_middle[-1])
#     sleep(5)
comp_enable.append(True)
comp_set_speed.append
print(len(comp_enable))
print(len(comp_set_speed))
