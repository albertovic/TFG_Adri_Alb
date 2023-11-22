#!/usr/bin/python
#To run this script use:
#sudo python3 multiple_sensors.py --device /dev/ttyAMA4
#When echosounder connected to serial 4


#IMPORTS BEGIN
#-------------------------------
#Imports for temperature sensor
import os
import tsys01

#Imports for pressure sensor
import sensor_codes.multiple_sensors_pkg.examples.ms5837 as ms5837

#Imports for echosounder sensor (altimeter)
from brping import Ping1D
import argparse
from builtins import input

#Common imports
import time
#-------------------------------
#IMPORTS END



#PARSE COMMAND LINE OPTIONS BEGIN
#-------------------------------
parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
args = parser.parse_args()
if args.device is None and args.udp is None:
    parser.print_help()
    exit(1)
#-------------------------------
#END OF PARSE COMMAND LINE OPTIONS



#CREATION OF THE SENSORS OBJECTS BEGIN
#-------------------------------
temp_sensor = tsys01.TSYS01(6) #We need to specify the rapberry bus (6). 
#The bus number can be obtained using the command i2cdetect -y 6

press_sensor = ms5837.MS5837_30BA(6) #This object creation lets us specify the model and the bus number

echo_sensor = Ping1D()
if args.device is not None:
    echo_sensor.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    echo_sensor.connect_udp(host, int(port))
#-------------------------------
#END OF SENSORS OBJECTS CREATION



#OBJECT CREATION ERROR TREATMENT BEGIN
#-------------------------------
if not temp_sensor.init():
    print("Temperature sensor could not be initialized")
    exit(1)

if not press_sensor.init():
        print("Pressure sensor could not be initialized")
        exit(1)

if echo_sensor.initialize() is False:
    print("Echosounder sensor could not be initialized")
    exit(1)
#-------------------------------
#ENF OF OBJECT CREATION ERROR TREATMENT



#SENSORS READING BEGIN
#-------------------------------
print("------------------------------------")
print("All sensors correctly initialized...")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to start measurement...")

while True:

    #Temperature sensor reading
    if not temp_sensor.read():
        print("Error reading temperature sensor")
        exit(1)
    print("Temperature sensor: \n   Temperature: %.2f C\t%.2f F" % (temp_sensor.temperature(), temp_sensor.temperature(tsys01.UNITS_Farenheit)))

    #Pressure sensor reading
    if press_sensor.read():    #he cambiado a grados C por defecto en el sensor pressure, si queremos otra unidad sensor.pressure(UNITS_psi)
            print(("Pressure sensor: \n   Pressure: %0.2f atm   Temperature: %0.2f ºC")%(press_sensor.pressure(),press_sensor.temperature()))
    else:
            print("Error reading pressure sensor")
            exit(1)

    #Echosounder sensor reading
    data = echo_sensor.get_distance()
    if data:
        print("Echosounder sensor: \n   Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Error reading echosounder sensor")

    time.sleep(1)
    os.system ("clear")
#-------------------------------
#SENSORS READINGS END
