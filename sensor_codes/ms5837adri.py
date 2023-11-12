##código prueba ADRI sensor ms5837
import ms5837
import time
#para probar si el programa sale del bucle pulsando una tecla importamos
#import keyboard
##HE CAMBIADO EN EL CÓDIGO DE ms5837 LOS BUSES A 6 Y ESTABAN A 1
sensor = ms5837.MS5837_30BA(6) #de esta manera especificamos el modelo y el bus
#he comprobado con i2cdetect -y 6 que es el 6 el bus correcto, comprobar cada vez que se en>

# We must initialize the sensor before reading it
if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)
# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)
#print de la presión con la función .pressure
print(("Presión: %.2f atm") % (sensor.pressure(ms5837.UNITS_atm)))
#print de la temperatura con la función .temperature
print(("Temperature: %.2f C") % (sensor.temperature(ms5837.UNITS_Centigrade)))
print(("MSL Relative Altitude: %.2f metros") % sensor.altitude()) # relative to Mean Sea Le>
time.sleep(5)
while True:
   # if keyboard.is_pressed('x'):
       # print('Se ha detenido la lectura de datos')
       # break
