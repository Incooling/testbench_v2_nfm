import compressor
import hvac
import valve
from MX100QP import *
from time import sleep
from setup import *
import threads


def set_bench():
    while True:

        command = input("Do you want to activate inhouse? ")
        if command == "yes":
            print("setting all devices this might take 1min")
            print("Enabling power supplies")

            # Pressure sensors
            print("Enabling pressure sensors")
            ttiPsu.setTargetVolts(2, 12)
            ttiPsu.setOutputEnable(2, True)

            # Expansion valve
            print("Enabling eev")
            ttiPsu.setTargetVolts(3, 12)
            ttiPsu.setOutputEnable(3, True)

            # Flowmeter
            # print("Enabling flowmeter")

            print("Wait till all devices have connected to internet")
            sleep(20)

            # Valve
            print("Current valve position", valve.getValvePos())
            print("Setting valve")
            valve.setValvePos(18)

            # Wait till valve reached position
            # while True:
            #     if valve.target_reached() == True:
            #         break

            # fans
            print("Enabling fans")
            fan_set_var.insert(0, ttiPsu.setTargetVolts(1, 12))
            ttiPsu.setOutputEnable(1, True)

            # HVAC
            print("Enabling HVAC")
            hvac_set_var.insert(0, hvac.setHVAC(0))
            comp_set_var.insert(0, compressor.setCompressor(1.5))

            # compressor
            print("Enabling compressor")
            compressor.setQPX1200SP_1(24, 1)
            comp_enable_var.insert(0, (compressor.setEnable(True)))

            threads.update_monitor.start()
            break
