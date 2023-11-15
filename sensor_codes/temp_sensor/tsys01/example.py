#!/usr/bin/python
#para correr este programa utilizar python3 example.py
import tsys01
from time import sleep

sensor = tsys01.TSYS01(6) #hace falta especificar el bus de la raspberry que es la 6 (es el del navigator). Se puede comprobar con el i2cdetect -y 6

if not sensor.init():
    print("Error initializing sensor")
    exit(1)

while True:
    if not sensor.read():
        print("Error reading sensor")
        exit(1)
    print("Temperature: %.2f C\t%.2f F" % (sensor.temperature(), sensor.temperature(tsys01.UNITS_Farenheit))) #en el github hay un parentesis mal, cuidado al clonarlo
    sleep(0.2)
