
##código prueba ADRI sensor ms5837
import ms5837
import time
import os
#para probar si el programa sale del bucle pulsando una tecla importamos
#import keyboard
##HE CAMBIADO EN EL CÓDIGO DE ms5837 LOS BUSES A 6 Y ESTABAN A 1
sensor = ms5837.MS5837_30BA(6) #de esta manera especificamos el modelo y el bus
#he comprobado con i2cdetect -y 6 que es el 6 el bus correcto, comprobar cada vez que se enciende, no se si cambia

# We must initialize the sensor before reading it
if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)


# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

   
#time.sleep(2)

while True:


    if sensor.read():    #he cambiado a grados C por defecto en el sensor pressure, si queremos otra unidad sensor.pressure(UNITS_psi)
            print(("PRESIÓN: %0.2f atm      TEMPERATURA: %0.2f ºC")%(sensor.pressure(),sensor.temperature()))
            time.sleep(1)
            os.system('clear')    

    else:
            print("Error leyendo el sensor")
            exit(1)
