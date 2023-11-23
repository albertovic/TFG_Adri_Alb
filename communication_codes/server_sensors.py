#!/usr/bin/env python3

#IMPORTS BEGIN
#-------------------------------
#Imports for temperature sensor
import os
import tsys01

#Imports for pressure sensor
import ms5837

#Imports for echosounder sensor (altimeter)
from brping import Ping1D
import argparse
from builtins import input

#Common imports
import time
import socket
import threading
#-------------------------------
#IMPORTS END


sensor_data = {}
host_ip = "192.168.2.2"
port_id = 12345



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
def read_sensors():
    while True:

    #Temperature sensor reading
        if not temp_sensor.read():
            print("Error reading temperature sensor")
            exit(1)
        sensor_data['T_temp'] = temp_sensor.temperature()
    
    #Pressure sensor reading
        if press_sensor.read():    #he cambiado a grados C por defecto en el sensor pressure, si queremos otra unidad sensor.pressure(UNITS_psi)
            sensor_data['P_pressure'] = press_sensor.pressure()
            sensor_data ['P_temp'] = press_sensor.temperature()
        else:
            print("Error reading pressure sensor")
            exit(1)

    #Echosounder sensor reading
        data = echo_sensor.get_distance()
        if data:
            sensor_data['E_distance'] = data["distance"]
            sensor_data['E_confidence'] = data["confidence"]
        else:
            print("Error reading echosounder sensor")

        time.sleep(1)
        os.system ("clear")
    
    #Internal temperature reading
        try:
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as archivo_temp:
                        temp_raw = int(archivo_temp.readline().strip())
                        temp = temp_raw / 1000.0
                        sensor_data['R_temp'] = temp
        except FileNotFoundError:
                return "No se pudo leer la temperatura"
#-------------------------------
#SENSORS READINGS END

def data_print(sensor_data):
    data_string = "Temperature sensor:\n"
    data_string += "Temperature: %.2f C\n" % (sensor_data['T_temp'])
    data_string += "Pressure sensor:\n"
    data_string += "Temperature: %.2f C   Pressure: %.2f atm\n" % (sensor_data['P_temp'], sensor_data['P_pressure'])
    data_string += "Internal temperature sensor:\n"
    data_string += "Temperature: %.2f C\n" % (sensor_data['R_temp'])
    data_string += "Echosounder sensor:\n"
    data_string += "Distance: %s   Confidence: %s%%\n" % (sensor_data["E_distance"], sensor_data["E_confidence"])
    return data_string
                
class Server:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host_ip, port_id))
            self.server_socket.listen(1)
            print(f"El servidor esta escuchando en {self.host}:{self.port}")

        def start(self):
            client_socket, addr = self.server_socket.accept()
            print(f"Conexion establecida con {addr}")

            while True:
                    data = client_socket.recv(1024)
                    if not data:
                            break
                    print(f"Mensaje recibido de {addr}: {data.decode()}")
                    datos = data_print(sensor_data)
                    client_socket.sendall(datos.encode())
            print(f"Conexión cerrada con {addr}")
            client_socket.close()

       
if __name__ == "__main__":
        server = Server(host_ip, port_id)
        sensors_thread = threading.Tread(target=read_sensors)
        sensors_thread.start()

        socket_thread = threading.Thread(target=server.start)
        server.start()
