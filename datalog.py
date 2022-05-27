from setup import *
import datetime

file

def log_data(i, temp_data, pressure_data, fan_data, valve_data, hvac_data, compressor_data, humidity_data):
    date.insert(0, datetime.datetime.now().strftime("%d-%b-%Y"))  # file[2]
    date.insert(1, datetime.datetime.now().strftime("%H:%M:%S"))  # file[3]

    # # Input data into columns
    sheet1.write(i, date_colm, date[0])
    sheet1.write(i, time_colm, date[1])
    sheet1.write(i, name_colm, file[0])
    sheet1.write(i, desciption_colm, file[1])
    sheet1.write(i, mac_qpx1200sp1, QPX1200SP1_mac)
    sheet1.write(i, mac_qpx1200sp2, QPX1200SP2_mac)
    sheet1.write(i, mac_mx1000qp_colm, MX100QP_mac)
    sheet1.write(i, mac_nanotec_colm, nanoTec_mac)
    sheet1.write(i, mac_tektronix_colm, MDO3024_mac)
    sheet1.write(i, mac_daq970_colm, DAQ970A_mac)
    sheet1.write(i, mac_bronkhorst_colm, 1)
    sheet1.write(i, mac_omega_colm, 1)  # setup.ttiPsu.getOutputVolts(3))
    sheet1.write(i, iteration_colm, i)
    sheet1.write(i, fan_volt_colm, fan_data['fan_volt'])
    sheet1.write(i, fan_cur_colm, fan_data['fan_cur'])
    sheet1.write(i, fan_speed_colm, fan_data['fan_freq'])
    sheet1.write(i, t_evap_in_colm, temp_data['t_evap_in'])
    sheet1.write(i, t_evap_out_colm, temp_data['t_evap_out'])
    sheet1.write(i, t_evap_out_mid_colm, temp_data['t_evap_out_mid'])
    sheet1.write(i, t_cond_in_colm, temp_data['t_cond_in'])
    if flowmeter_use[0]:
        sheet1.write(i, t_cond_out_colm, temp_data['t_cond_out_flow'])
    else:
        sheet1.write(i, t_cond_out_colm, temp_data['t_cond_out'])
    sheet1.write(i, t_flow_out_colm, temp_data['t_flow_out'])
    sheet1.write(i, press4_colm, pressure_data['p_flow_out'])
    sheet1.write(i, press3_colm, pressure_data['p_cond_in'])
    sheet1.write(i, press2_colm, pressure_data['p_evap_out'])
    sheet1.write(i, valve_pos_colm, valve_data['position'])
    sheet1.write(i, mass_flow_colm, "disabled")
    sheet1.write(i, temp_flow_colm, "disabled")
    sheet1.write(i, dens_flow_colm, "disabled")
    sheet1.write(i, press_flow_colm, 1)
    sheet1.write(i, heat_diss_vol_colm, hvac_data['hvac_volt'])
    sheet1.write(i, heat_diss_cur_colm, hvac_data['hvac_cur'])
    sheet1.write(i, heat_diss_power_colm, "")
    sheet1.write(i, comp_volt_colm, compressor_data['comp_volt_supply'])
    sheet1.write(i, comp_cur_in_colm, compressor_data['comp_cur_supply'])
    sheet1.write(i, comp_power_colm, "")
    sheet1.write(i, comp_rpm_colm, 1)
    sheet1.write(i, comp_rpm_max_colm, 1)
    sheet1.write(i, comp_rpm_min_colm, 1)
    sheet1.write(i, comp_rpm_avg_colm, 1)
    sheet1.write(i, comp_rpm_dev_colm, "")
    sheet1.write(i, comp_status_colm, compressor_data['comp_status'])
    sheet1.write(i, comp_overheat_colm, compressor_data['comp_overheat'])
    sheet1.write(i, comp_enable_colm, compressor_data['comp_enable'])
    sheet1.write(i, comp_cur_out_colm, compressor_data['comp_cur_board'])
    sheet1.write(i, comp_speed_in_colm, compressor_data['comp_set_speed'])
    sheet1.write(i, humidity_colm, humidity_data['humidity'])
    sheet1.write(i, ambient_temp_colm, temp_data['t_load_ambient'])
    sheet1.write(i, temp_load_1_colm, temp_data['t_load_inlet'])
    sheet1.write(i, temp_load_2_colm, temp_data['t_load_middle'])
    sheet1.write(i, temp_load_3_colm, temp_data['t_load_out'])
    sheet1.write(i, set_heat_load_colm, hvac_data['hvac_set'])
    sheet1.write(i, flowmeter_setting_colm, 1) # flowmeter_data['setting']

    wb1.save(f'{file[0]}.xls')
