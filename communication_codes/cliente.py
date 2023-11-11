#!/usr/bin/env python3

#Code used as an example of a client using sockets. This was made in the initial steps of the project in order to deeply 
#understand the socket library.

import socket
import asyncio

#IP OrangePi
#host_ip = "192.168.1.30"

#IP RaspberryPi
host_ip = ""
port_id = 12345

class Client:

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((self.host, self.port))
		print(f"Conexion establecida con {self.host}:{self.port}")
		

	async def send_message(self, message):
		while True:
			message = 'Dame los datos'
			self.client_socket.sendall(message.encode())
			data = self.client_socket.recv(1024)
			print('Respuesta del servidor:', data.decode())
			await asyncio.sleep(3)

	def close(self):
		self.client_socket.close()

if __name__ == "__main__":
	client = Client(host_ip, port_id)

	while True:
		message = 'Hola, servidor!'
		asyncio.run(client.send_message(message))

	#client.close()
