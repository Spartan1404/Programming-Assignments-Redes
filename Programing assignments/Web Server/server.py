#import socket module
from socket import *

#create a tcp server socket
#AF_INET is used for ipv4 protocol
#SOCK_STREAM is used for tcp
serverSocket = socket(AF_INET, SOCK_STREAM)
#the port must be >1024 because permission denied
serverPort=3000

#Prepare a sever socket
#Bind the socket to aserver address and server port
serverSocket.bind(('10.0.0.2',serverPort))

#listen to at most 1 connection
serverSocket.listen(1)
print('the web server is up on port:',serverPort)

while True:
	#Ser up a new connection from the client
	print('Ready to serve...')
	connectionSocket, addr = serverSocket.accept()

	try:
		#recieve the request message from the client
		message = connectionSocket.recv(1024)
		#print(message,'::',message.split()[0],':',message.split()[1])
		
		#extract the path of the requested object from the meassage
		#the path is the second part of the http header identified as [1]
		filename = message.split()[1]
		#print(filename,'||',filename[1:])
		
		# because the extracted path of the request has a / we read from the 2nd char
		f = open(filename[1:])
		outputdata = f.read()
		#Send one HTTP header line into socket
		#Fill in start
		connectionSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n','UTF-8'))
		
		#Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			connectionSocket.send(bytes(outputdata[i],'UTF-8'))
		connectionSocket.send(bytes("\r\n",'UTF-8'))
		connectionSocket.close()
	except IOError:
		#Send response message for file not found
		print('file not found')
		connectionSocket.send(bytes('\nHTTP/1.1 404 Not Found\n\n','UTF-8'))
		connectionSocket.send(bytes('<html><head><title>First Web Page</title></head><body><h1>404 Not Found</h1></body></html>\r\n','UTF-8'))
		connectionSocket.close()
