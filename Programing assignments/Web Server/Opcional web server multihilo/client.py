from socket import *
import sys

server_host = sys.argv[1]
server_port = int(sys.argv[2])
filename = sys.argv[3]

server_address = (server_host, server_port)
try:
	client_socket = socket(AF_INET,SOCK_STREAM)
	client_socket.connect(server_address)
	print('conectado a: ', server_address)
	
	request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
	client_socket.sendall(request.encode())

except IOError:
	print("el cliente ha caido")
	sys.exit(1)
	
final=""
while True:
	data = client_socket.recv(1024)
	if not data:
		break
	final += data.decode()

client_socket.close()
print("The data: ",final)
