from threads import *
from plot import *
from testbench import *

# Humidity
print("Enabling humidity")
ttiPsu.setTargetVolts(4, 15)
ttiPsu.setOutputEnable(4, True)
ttiPsu.setTargetAmps(4, 1)

file_name = input("Give file name: ")
file.insert(0, file_name)
file_description = input("Give file description: ")
file.insert(1, file_description)
command = input("Do you want to use the flowmeter? ")

if command == "yes":
    flowmeter_use.insert(0, True)
else:
    flowmeter_use.insert(0, False)

update_data.start()
update_bench.start()

if __name__ == '__main__':
    # animate
    ani = FuncAnimation(fig, update_graph,
                        fargs=(date_plot, t_load_middle_plot, t_evap_in_plot, t_evap_out_plot, t_cond_in_plot,
                               t_cond_out_plot, p_flow_out_plot, p_cond_in_plot, p_evap_out_plot, valve_position_plot,
                               flowmeter_density_plot, flowmeter_flow_plot, t_delta_evap_plot, w_heat_load_plot), interval=1000)
    plt.show()
