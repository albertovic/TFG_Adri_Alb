#!/usr/bin/env python3

import socket

host_ip = "192.168.1.30"
port_id = 12345

def leer_temp():
        try:
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as archivo_temp:
                        temp_raw = int(archivo_temp.readline().strip())
                        temp = temp_raw / 1000.0
                        return temp
        except FileNotFoundError:
                return "No se pudo leer la temperatura"
                
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
                    temperatura = leer_temp()
                    client_socket.sendall(f"Temperatura = {temperatura}".encode())
            print(f"Conexión cerrada con {addr}")
            client_socket.close()

       
if __name__ == "__main__":
        server = Server(host_ip, port_id)
        server.start()
