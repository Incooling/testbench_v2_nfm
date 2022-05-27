from time import sleep
import compressor
import hvac
import valve
from MX100QP import *
import os
from setup import *


def start_monitor():
    while True:
        print("Type /stop/ if you want to terminate logging and shut down devices")
        print("Type /device/ if you want to change a device setting or /test/ if you want to start a test")
        command = input()  # Give user input
        if command == "stop":
            hvac.setHVAC(0)
            compressor.setEnable(False)
            compressor.setCompressor(0)
            ttiPsu.setOutputEnable(1, False)
            valve.setValvePos(0)



            print("Exiting program, Ciao Markos")

            os._exit(0)

        if command == "test":
            command = input("Which test do you want to run?: ")  # Give user input

            if command == "fan":
                print("fan")

                for x in range(50, 140, 1):
                    ttiPsu.setTargetVolts(1, x / 10)
                    ttiPsu.setOutputEnable(1, True)
                    sleep(5)

            if command == "hvac":
                print("hvac")

                for voltage in range(500, 0, 5):
                    hvac_set_var.insert(0, hvac.setHVAC(voltage / 10))
                    sleep(5)

            if command == "compressor":

                voltage = 0.9
                while True:
                    comp_set_var.insert(0, compressor.setCompressor(voltage))
                    comp_enable_var.insert(0, compressor.setEnable(True))

                    voltage += 0.1
                    print("voltage", voltage)
                    sleep(60)

        if command == "device":
            command = input("Which device do you want to set?: ")  # Give user input

            if command == "hvac":
                power = float(input("Set HVAC power "))
                hvac_set.append(hvac.setHVAC(power))

            if command == "compressor":
                voltage = float(input("Set compressor voltage: "))
                comp_set_speed.append(compressor.setCompressor(voltage))

            if command == "valve":
                print("Current position: ", valve.getValvePos())  # User can retrieve current position from the
                # controller dictionary
                posInput = int(input("Set target position: "))  # Give user input
                print("Setting valve might take some time")
                valve.setValvePos(posInput)  # Final function to set the position of the valve
                # Wait till valve reached position




            if command == "fan":
                voltage = float(input("Set fan voltage: "))
                ttiPsu.setTargetVolts(1, voltage)

                sleep(2)
