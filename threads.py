import threading

import measurement
import command
import testbench

update_monitor = threading.Thread(name='command', target=command.start_monitor)
update_data = threading.Thread(name='plot', target=measurement.update_data)
update_bench = threading.Thread(name='testbench', target=testbench.set_bench)
# update_data_hvac = threading.Thread(name='testbench', target=measurement.get_data_hvac)

update_monitor.daemon = True
update_data.daemon = True
update_bench.daemon = True
# update_data_hvac.daemon = True
