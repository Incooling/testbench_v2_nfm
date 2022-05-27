import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy
import numpy as np
from matplotlib.animation import FuncAnimation
import collections
import datetime as dt
from setup import *

date_plot = [0] * samples
t_load_middle_plot = [0] * samples
t_evap_in_plot = [0] * samples
t_evap_out_plot = [0] * samples
t_cond_in_plot = [0] * samples
t_cond_out_plot = [0] * samples
p_flow_out_plot = [0] * samples
p_cond_in_plot = [0] * samples
p_evap_out_plot = [0] * samples
valve_position_plot = [0] * samples
flowmeter_density_plot = [0] * samples
flowmeter_flow_plot = [0] * samples
t_delta_evap_plot = [0] * samples
t_cond_out_flow_plot = [0] * samples
t_flow_out_plot = [0] * samples
w_heat_load_plot = [0] * samples


# function to update the data
def update_graph(i, date_plot, t_load_middle_plot, t_evap_in_plot, t_evap_out_plot, t_cond_in_plot,
                 t_cond_out_plot, p_flow_out_plot, p_cond_in_plot, p_evap_out_plot, valve_position_plot,
                 t_delta_evap_plot, t_cond_out_flow_plot,
                 t_flow_out_plot, w_heat_load_plot):
    # get data
    date_plot.append(dt.datetime.now().strftime('%H:%M:%S'))
    date_plot = date_plot[-samples:]

    t_load_middle_plot.append(t_load_middle[0])
    t_load_middle_plot = t_load_middle_plot[-samples:]
    ax_t_load_middle.clear()

    t_evap_in_plot.append(t_evap_in[0])
    t_evap_in_plot = t_evap_in_plot[-samples:]
    ax_t_evap_in.clear()

    t_evap_out_plot.append(t_evap_out[0])
    t_evap_out_plot = t_evap_out_plot[-samples:]
    ax_t_evap_out.clear()

    t_cond_in_plot.append(t_cond_in[0])
    t_cond_in_plot = t_cond_in_plot[-samples:]
    ax_t_cond_in.clear()

    t_cond_out_plot.append(t_cond_out[0])
    t_cond_out_plot = t_cond_out_plot[-samples:]
    ax_t_cond_out.clear()

    t_cond_out_flow_plot.append(t_cond_out_flow[0])
    t_cond_out_flow_plot = t_cond_out_flow_plot[-samples:]
    ax_t_cond_out_flow.clear()

    t_flow_out_plot.append(t_flow_out[0])
    t_flow_out_plot = t_flow_out_plot[-samples:]
    ax_t_flow_out.clear()

    p_flow_out_plot.append(p_flow_out[0])
    p_flow_out_plot = p_flow_out_plot[-samples:]
    ax_p_flow_out.clear()

    p_cond_in_plot.append(p_cond_in[0])
    p_cond_in_plot = p_cond_in_plot[-samples:]
    ax_p_cond_in.clear()

    p_evap_out_plot.append(p_evap_out[0])
    p_evap_out_plot = p_evap_out_plot[-samples:]
    ax_p_evap_out.clear()

    valve_position_plot.append(valve_position[0])
    valve_position_plot = valve_position_plot[-samples:]
    ax_valve_opening.clear()

    w_heat_load_plot.append(round(hvac_volt[0]*hvac_cur[0], 2))
    w_heat_load_plot = w_heat_load_plot[-samples:]
    ax_w_heat_load.clear()

    t_delta_evap_plot.append(round((t_evap_out[0] - t_sat_evap_in[0]), 2))
    t_delta_evap_plot = t_delta_evap_plot[-samples:]
    ax_t_delta_evap.clear()

    ax_t_load_middle.plot(date_plot, t_load_middle_plot, color='y', zorder=1, label='t_load')
    ax_t_load_middle.scatter(date_plot[-1:], t_load_middle_plot[-1:])
    ax_t_load_middle.text(date_plot[-1], t_load_middle[0], "  {}".format(t_load_middle[0], ha='right', size='medium'))
    ax_t_load_middle.legend(loc="upper left")
    ax_t_load_middle.tick_params(axis='x', labelrotation=45)

    ax_t_evap_in.plot(date_plot, t_evap_in_plot, color='b', zorder=1, label="t_evap_in")
    ax_t_evap_in.scatter(date_plot[-1:], t_evap_in_plot[-1:])
    ax_t_evap_in.text(date_plot[-1], t_evap_in[0], "  {}".format(t_evap_in[0], ha='right', size='medium'))
    ax_t_evap_in.legend(loc="upper left")
    ax_t_evap_in.tick_params(axis='x', labelrotation=45)

    ax_t_evap_out.plot(date_plot, t_evap_out_plot, color='r', zorder=1, label='t_evap_out')
    ax_t_evap_out.scatter(date_plot[-1:], t_evap_out_plot[-1:])
    ax_t_evap_out.text(date_plot[-1], t_evap_out[0], "  {}".format(t_evap_out[0], ha='right', size='medium'))
    ax_t_evap_out.legend(loc="upper left")
    ax_t_evap_out.tick_params(axis='x', labelrotation=45)

    ax_t_delta_evap.plot(date_plot, t_delta_evap_plot, color='b', zorder=1, label='t_delta_evap')
    ax_t_delta_evap.scatter(date_plot[-1:], t_delta_evap_plot[-1:])
    ax_t_delta_evap.text(date_plot[-1], t_delta_evap_plot[-1], "  {}".format(t_delta_evap_plot[-1], ha='right', size='medium'))
    ax_t_delta_evap.legend(loc="upper left")
    ax_t_delta_evap.tick_params(axis='x', labelrotation=45)

    ax_t_cond_in.plot(date_plot, t_cond_in_plot, color='b', zorder=1, label="t_cond_in")
    ax_t_cond_in.scatter(date_plot[-1:], t_cond_in_plot[-1:])
    ax_t_cond_in.text(date_plot[-1], t_cond_in_plot[-1], "  {}".format(t_cond_in_plot[-1], ha='right', size='medium'))
    ax_t_cond_in.legend(loc="upper left")
    ax_t_cond_in.tick_params(axis='x', labelrotation=45)

    if flowmeter_use[0]:
        ax_t_cond_out.plot(date_plot, t_cond_out_flow_plot, color='r', zorder=1, label="t_cond_out_flow")
        ax_t_cond_out.scatter(date_plot[-1:], t_cond_out_flow_plot[-1:])
        ax_t_cond_out.text(date_plot[-1], t_cond_out_flow_plot[-1], "  {}".format(t_cond_out_flow_plot[-1], ha='right', size='medium'))
        ax_t_cond_out.legend(loc="upper left")
        ax_t_cond_out.tick_params(axis='x', labelrotation=45)

        ax_t_cond_out.plot(date_plot, t_flow_out_plot, color='g', zorder=1, label="t_flow_out")
        ax_t_cond_out.scatter(date_plot[-1:], t_flow_out_plot[-1:])
        ax_t_cond_out.text(date_plot[-1], t_flow_out_plot[-1], "  {}".format(t_flow_out_plot[-1], ha='right', size='medium'))
        ax_t_cond_out.legend(loc="upper left")
        ax_t_cond_out.tick_params(axis='x', labelrotation=45)
    else:
        ax_t_cond_out.plot(date_plot, t_cond_out_plot, color='r', zorder=1, label="t_cond_out")
        ax_t_cond_out.scatter(date_plot[-1:], t_cond_out_plot[-1:])
        ax_t_cond_out.text(date_plot[-1], t_cond_out_plot[-1], "  {}".format(t_cond_out_plot[-1], ha='right', size='medium'))
        ax_t_cond_out.legend(loc="upper left")
        ax_t_cond_out.tick_params(axis='x', labelrotation=45)

    ax_p_flow_out.plot(date_plot, p_flow_out_plot, color='b', zorder=1, label="p_flow_out")
    ax_p_flow_out.scatter(date_plot[-1:], p_flow_out_plot[-1:])
    ax_p_flow_out.text(date_plot[-1], p_flow_out_plot[-1], "  {}".format(p_flow_out_plot[-1], ha='right', size='medium'))
    ax_p_flow_out.legend(loc="upper left")
    ax_p_flow_out.tick_params(axis='x', labelrotation=45)

    ax_p_cond_in.plot(date_plot, p_cond_in_plot, color='r', zorder=1, label="p_cond_in")
    ax_p_cond_in.scatter(date_plot[-1:], p_cond_in_plot[-1:])
    ax_p_cond_in.text(date_plot[-1], p_cond_in_plot[-1], "  {}".format(p_cond_in_plot[-1], ha='right', size='medium'))
    ax_p_cond_in.legend(loc="upper left")
    ax_p_cond_in.tick_params(axis='x', labelrotation=45)

    ax_p_evap_out.plot(date_plot, p_evap_out_plot, color='g', zorder=1, label="p_evap_out")
    ax_p_evap_out.scatter(date_plot[-1:], p_evap_out_plot[-1:])
    ax_p_evap_out.text(date_plot[-1], p_evap_out_plot[-1], "  {}".format(p_evap_out_plot[-1], ha='right', size='medium'))
    ax_p_evap_out.legend(loc="upper left")
    ax_p_evap_out.tick_params(axis='x', labelrotation=45)

    ax_w_heat_load.plot(date_plot, w_heat_load_plot, color='g', zorder=1, label="power_heat_load")
    ax_w_heat_load.scatter(date_plot[-1:], w_heat_load_plot[-1:])
    ax_w_heat_load.text(date_plot[-1], w_heat_load_plot[-1], "  {}".format(w_heat_load_plot[-1], ha='right', size='medium'))
    ax_w_heat_load.legend(loc="upper left")
    ax_w_heat_load.tick_params(axis='x', labelrotation=45)

    ax_valve_opening.plot(date_plot, valve_position_plot, color='b', zorder=1, label='valve_opening')
    ax_valve_opening.scatter(date_plot[-1:], valve_position_plot[-1:])
    ax_valve_opening.text(date_plot[-1], valve_position_plot[-1], "  {}".format(valve_position_plot[-1], ha='right', size='medium'))
    ax_valve_opening.legend(loc="upper left")
    ax_valve_opening.tick_params(axis='x', labelrotation=45)

# define and adjust figure
fig = plt.figure(figsize=(150, 30), facecolor='#A9A9A9')
# set the spacing between subplots
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.136,
                    hspace=0.4)

ax_t_load_middle = plt.subplot(331)
ax_t_evap_in = plt.subplot(332)
ax_t_evap_out = plt.subplot(332)
ax_t_delta_evap = plt.subplot(333)
ax_t_cond_in = plt.subplot(334)
ax_t_cond_out = plt.subplot(334)
ax_t_cond_out_flow = plt.subplot(334)
ax_t_flow_out = plt.subplot(334)
ax_p_flow_out = plt.subplot(335)
ax_p_cond_in = plt.subplot(335)
ax_p_evap_out = plt.subplot(335)
ax_w_heat_load = plt.subplot(336)
ax_valve_opening = plt.subplot(337)

ax_t_load_middle.set_facecolor('w')
ax_t_load_middle.set_facecolor('w')
ax_t_evap_in.set_facecolor('w')
ax_t_evap_out.set_facecolor('w')
ax_t_delta_evap.set_facecolor('w')
ax_t_cond_in.set_facecolor('w')
ax_t_cond_out.set_facecolor('w')
ax_p_flow_out.set_facecolor('w')
ax_p_cond_in.set_facecolor('w')
ax_p_evap_out.set_facecolor('w')
ax_w_heat_load.set_facecolor('w')
ax_valve_opening.set_facecolor('w')
