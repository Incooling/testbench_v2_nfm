import threading
import pyvisa
import xlwt as xw
from statemachine import StateMachine, State
from datetime import datetime
import socket

# Fan setup
# from command import Monitor


rm = pyvisa.ResourceManager()
# MAC addresses
MX100QP_mac = "80-E4-DA-20-98-C9"
DAQ970A_mac = "80-09-02-11-10-DB"
KEY_34461A_mac = "80-09-02-14-B2-7A"
nanoTec_mac = "44-AA-E8-00-4A-8E"
QPX1200SP1_mac = "80-E4-DA-20-9A-C7"
QPX1200SP2_mac = "80-E4-DA-20-9A-C4"
MDO3024_mac = "08:00:11:23:17:E4"
omega_mac = "00:03:34:03:27:2E"

# VISA/IP addresses
DAQM970A = 'TCPIP0::10.58.32.253::inst0::INSTR'
KEY_34461A = 'TCPIP0::10.58.32.249::inst0::INSTR'
MDO3024 = 'TCPIP0::10.58.32.251::inst0::INSTR'  # MDO3024
MX100QP = "10.58.32.254"  # MX100QP
QPX1200SP_1 = 'TCPIP0::10.58.32.252::9221::SOCKET'  # QPC1200SP
QPX1200SP_2 = 'TCPIP0::10.58.32.247::9221::SOCKET'  # QPC1200SP
omega = "10.58.32.248"
nanotec = "10.58.32.250"  # NanoTec
nanotec_port = 80  # NanoTec


## Nanotec controller
# init new connection
def initConnection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((nanotec, nanotec_port))

    return sock


# Target Position
indexTargetPos = "607A"
subindexTargetPos = "00"
bitLengtTargetPos = "10"

## Controlword
indexControlword = "6040"
subindexControlword = "00"
bitLengthControlword = "6"

valueControlwordMove = "001F"  # Move
valueControlwordOff = "0006"  # Shut down
valueControlwordOn = "0007"  # Switch on

# Position Actual Valve
indexPosValve = "6064"
subindexPosValve = "00"

# Position Actual Valve
indexTargetReached = "6041"
subindexTargetReached = "00"

## Datalog
global file_name
global flowmeter_use

hvac_data = dict()
temp_data = dict()

samples = 20

# Temperature array
t_evap_in = list()
t_evap_in = [0] * samples
t_evap_out = list()
t_cond_in = list()
t_cond_out = list()
t_cond_out_flow = list()
t_load_inlet = list()
t_load_middle = list()
t_load_out = list()
t_load_ambient = list()
t_flow_out = list()
t_sat_evap_in = list()
t_evap_out_mid = list()


# Pressure array
p_evap_out = list()
p_cond_in = list()
p_flow_out = list()

# Humidity array
humidity = list()

# Fan array
fan_freq = list()
fan_volt = list()
fan_cur = list()
fan_set_var = list()

# Flow array
flowmeter_flow = list()
flowmeter_temp = list()
flowmeter_density = list()
flowmeter_pressure = list()
flowmeter_setting = list()
flowmeter_setpoint = list()
flowmeter_fsetpoint = list()
flowmeter_setp_monitor = list()
flowmeter_setp_filter = list()
flowmeter_setp_slope = list()
flowmeter_control = list()
flowmeter_slave_factor = list()
flowmeter_fluid_num = list()
flowmeter_fluid_name = list()
flowmeter_valve_outp = list()
flowmeter_sensor = list()
flowmeter_capacity_100 = list()
flowmeter_capacity_0 = list()
flowmeter_cap_index = list()
flowmeter_cap_unit = list()
flowmeter_stable_resp = list()
flowmeter_sens_filter = list()
flowmeter_valve_state = list()
flowmeter_counter = list()
flowmeter_serial = list()
flowmeter_BHTModel = list()
flowmeter_firmware = list()
flowmeter_cust_model = list()
flowmeter_unipolair = list()
flowmeter_ind_number = list()
flowmeter_device_type = list()
flowmeter_use = list()

# Valve
valve_position = list()

# Compressor data
comp_status = list()
comp_overheat = list()
comp_cur_board = list()
comp_cur_supp = list()
comp_volt_supp = list()
comp_set_speed = list()
comp_enable = list()
comp_freq = list()
comp_max_freq = list()
comp_min_freq = list()
com_avg_freq = list()
comp_enable_var = list()
comp_set_var = list()


# HVAC
hvac_volt = list()
hvac_cur = list()
hvac_set = list()
hvac_set_var = list()
hvac_volt_update = list()
hvac_cur_update = list()
hvac_set_update = list()

# Humidity
humidity = list()

file = list()

t_load_middle = [0] * samples
t_evap_in = [0] * samples
t_evap_out = [0] * samples
p_flow_out = [0] * samples
p_cond_in = [0] * samples
p_evap_out = [0] * samples
valve_position = [0] * samples
flowmeter_density = [0] * samples
flowmeter_flow = [0] * samples
t_cond_in = [0] * samples
t_cond_out = [0] * samples
t_sat_evap_in = [0] * samples
t_cond_out_flow = [0] * samples
t_flow_out = [0] * samples
hvac_volt = [0] * samples
hvac_cur = [0] * samples

date = list()

flowmeter_use.insert(0, "")

date_colm = 0
time_colm = 1
name_colm = 2
desciption_colm = 3
mac_qpx1200sp1 = 4
mac_qpx1200sp2 = 5
mac_mx1000qp_colm = 6
mac_nanotec_colm = 7
mac_tektronix_colm = 8
mac_daq970_colm = 9
mac_bronkhorst_colm = 10
mac_omega_colm = 11
iteration_colm = 12
fan_volt_colm = 13
fan_cur_colm = 14
fan_speed_colm = 15
t_evap_in_colm = 16
t_evap_out_colm = 17
t_evap_out_mid_colm = 18
t_cond_in_colm = 19
t_cond_out_colm = 20
t_flow_out_colm = 21
press4_colm = 22
press3_colm = 23
press2_colm = 24
valve_pos_colm = 25
mass_flow_colm = 26
temp_flow_colm = 27
dens_flow_colm = 28
press_flow_colm = 29
heat_diss_vol_colm = 30
heat_diss_cur_colm = 31
heat_diss_power_colm = 32
comp_volt_colm = 33
comp_cur_in_colm = 34
comp_power_colm = 35
comp_rpm_colm = 36
comp_rpm_max_colm = 37
comp_rpm_min_colm = 38
comp_rpm_avg_colm = 39
comp_rpm_dev_colm = 40
comp_status_colm = 41
comp_overheat_colm = 42
comp_enable_colm = 43
comp_cur_out_colm = 44
comp_speed_in_colm = 45
humidity_colm = 46
ambient_temp_colm = 47
temp_load_1_colm = 48
temp_load_2_colm = 49
temp_load_3_colm = 50
set_heat_load_colm = 51
flowmeter_setting_colm = 52

# Workbook is created
wb1 = xw.Workbook()
wb2 = xw.Workbook()

# add_sheet is used to create sheet.
sheet1 = wb1.add_sheet('Sheet 1')

# Input data into rows
sheet1.write(0, 0, 'Date')
sheet1.write(0, 1, 'Time')
sheet1.write(0, 2, 'Test name')
sheet1.write(0, 3, 'Test description')
sheet1.write(0, 4, 'MAC QPX1200_1')
sheet1.write(0, 5, 'MAC QPX1200_2')
sheet1.write(0, 6, 'MAC MX1000QP fans/Fanotec')
sheet1.write(0, 7, 'MAC Nanotec')
sheet1.write(0, 8, 'MAC Tektronix')
sheet1.write(0, 9, 'MAC Keysight')
sheet1.write(0, 10, 'MAC flow meter')
sheet1.write(0, 11, 'MAC iBTHX-D')
sheet1.write(0, 12, 'Iteration number')
sheet1.write(0, 13, 'Fan voltage')
sheet1.write(0, 14, 'Fan current')
sheet1.write(0, 15, 'Fan speed')
sheet1.write(0, 16, 't_evap_in')
sheet1.write(0, 17, 't_evap_out')
sheet1.write(0, 18, 't_evap_out_mid')
sheet1.write(0, 19, 't_cond_in')
if flowmeter_use[0]:
    sheet1.write(0, 20, 't_cond_out_valve')
else:
    sheet1.write(0, 20, 't_cond_out')
sheet1.write(0, 21, "Temp flowmeter out ")
sheet1.write(0, 22, 'p_flowmeter_out')
sheet1.write(0, 23, 'p_cond_in')
sheet1.write(0, 24, 'p_evap_out')
sheet1.write(0, 25, 'Valve position')
sheet1.write(0, 26, 'Mass flowmeter')
sheet1.write(0, 27, 'Temp flowmeter')
sheet1.write(0, 28, 'Density flowmeter')
sheet1.write(0, 29, 'Pressure flowmeter')
sheet1.write(0, 30, 'Heat diss voltage')
sheet1.write(0, 31, 'Heat diss current')
sheet1.write(0, 32, 'Heat diss power')
sheet1.write(0, 33, 'Compressor voltage (mV)')
sheet1.write(0, 34, 'Compressor current (mA)')
sheet1.write(0, 35, 'Compressor power')
sheet1.write(0, 36, 'Compressor freq')
sheet1.write(0, 37, 'Comp freq max')
sheet1.write(0, 38, 'Comp freq min')
sheet1.write(0, 39, 'Comp freq avg ')
sheet1.write(0, 40, 'Comp freq dev')
sheet1.write(0, 41, 'Compressor status')
sheet1.write(0, 42, 'Compressor Overheat')
sheet1.write(0, 43, 'Compressor enable')
sheet1.write(0, 44, 'Compressor current out (V)')
sheet1.write(0, 45, 'Compressor speed inp')
sheet1.write(0, 46, 'Humidity')
sheet1.write(0, 47, 'Ambient temperature')
sheet1.write(0, 48, 't_load_inlet')
sheet1.write(0, 49, 't_load_middle')
sheet1.write(0, 50, 't_load_out')
sheet1.write(0, 51, 'Set HVAC voltage')
sheet1.write(0, 52, 'Setting flowmeter')


meas_unipolair_colm = 2
fmeas_colm = 3
setpoint_colm = 4
fsetpoint_colm = 5
setpoint_mon_colm = 6
setpoint_filter_colm = 7
setpoint_slope_colm = 8
controlmode_colm = 9
slave_fac_colm = 10
fluid_num_colm = 11
fluid_name_colm = 12
valve_outp_colm = 13
temp_colm = 14
density_colm = 15
sensor_type_colm = 16
capacity_100_colm = 17
capacity_0_colm = 18
capacity_index_colm = 19
capacity_unit_colm = 20
stable_resp_colm = 21
sens_filter_colm = 22
valve_safe_state_colm = 23
counter_mode_colm = 24
serial_colm = 25
BHTModel_colm = 26
firmware_colm = 27
customer_model_colm = 28
inden_number_colm = 29
device_type_colm = 30

sheet2 = wb2.add_sheet('Sheet 2')

sheet2.write(0, 0, 'Date')
sheet2.write(0, 1, 'Time')
sheet2.write(0, 2, 'Measure unipolair')
sheet2.write(0, 3, 'Fmeasure')
sheet2.write(0, 4, 'Setpoint')
sheet2.write(0, 5, 'Fsetpoint')
sheet2.write(0, 6, 'Setpoint monitor')
sheet2.write(0, 7, 'Setpoint filter ')
sheet2.write(0, 8, 'Setpoint slope')
sheet2.write(0, 9, 'Control mode')
sheet2.write(0, 10, 'Slave factor')
sheet2.write(0, 11, 'Fluid number')
sheet2.write(0, 12, 'Fluid name ')
sheet2.write(0, 13, 'Valve output')
sheet2.write(0, 14, 'Temperature')
sheet2.write(0, 15, 'Density')
sheet2.write(0, 16, 'Sensor type')
sheet2.write(0, 17, 'Capacity 100')
sheet2.write(0, 18, 'Capacity 0')
sheet2.write(0, 19, 'Capacity index unit')
sheet2.write(0, 20, 'Capacity unit')
sheet2.write(0, 21, 'Stable response')
sheet2.write(0, 22, 'Sensor filter')
sheet2.write(0, 23, 'Valve safe state')
sheet2.write(0, 24, 'Counter mode ')
sheet2.write(0, 25, 'Serial number')
sheet2.write(0, 26, 'BHTModel')
sheet2.write(0, 27, 'Firmware')
sheet2.write(0, 28, 'Customer model')
sheet2.write(0, 29, 'Identification number')
sheet2.write(0, 30, 'Device type')
