from socket import *
import threading

class ClientThread(threading.Thread):
	def __init__(self, connect, address):
		threading.Thread.__init__(self)
		self.connectionSocket = connect
		self.addr = address
		print('nueva conexion', address)
	def run(self):
	
		while True:
			try:
				message = self.connectionSocket.recv(1024)
				if not message:
					break
				print("\nmessage: ", message)
				data = str(message.decode())
				print("\ndecode: ", data)
				filename = data.split()[1]
				print("\nfilename:", filename[0:])
				f = open(filename[0:])
				outputdata = f.read()
				
				connectionSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n','UTF-8'))
				for i in range(0, len(outputdata)):
					connectionSocket.send(bytes(outputdata[i],'UTF-8'))
				connectionSocket.send(bytes("\r\n",'UTF-8'))
				connectionSocket.shutdown(SHUT_WR)
				
			except IOError:
				self.connectionSocket.send(bytes('HTTP/1.1 404 Not Found\r\n\r\n','UTF-8'))
				self.connectionSocket.send(bytes('<html><head><title>First Web Page</title></head><body><h1>404 Not Found</h1></body></html>\r\n','UTF-8'))
				connectionSocket.shutdown(SHUT_WR)
				

if __name__ == '__main__':
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverPort = 5000
	serverSocket.bind(('10.0.0.2',serverPort))
	serverSocket.listen(5)
	threads=[]
	while True:
		try:
			print('Ready to serve...')
			connectionSocket, addr = serverSocket.accept()
			client_thread = ClientThread(connectionSocket,addr)
			client_thread.daemon = True
			client_thread.start()
			threads.append(client_thread)
		except error:
			print("socket error")
			break
	serverSocket.close()
