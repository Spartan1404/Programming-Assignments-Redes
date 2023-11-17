from socket import *
import datetime
import threading

class ClientThread(threading.Thread):
	def __init__(self, connect, address):
		threading.Thread.__init__(self)
		self.connectionSocket = connect
		self.addr = address
	def run(self):
		while True:
			try:
				message = connectionSocket.recv(1024)
				if not message:
					break
				print "message: \n", message
				filename = message.split()[1]
				f = open(filename[1:])
				outputdata = f.read() 
				print "outputdata:", outputdata
				now = datetime.datetime.now() 
				#Send one HTTP header line into socket
				first_header = "HTTP/1.1 200 OK"
				# alive ={
				# 	"timeout":10,
				# 	"max":100,
				# }
				header_info = {
					# "Date": now.strftime("%Y-%m-%d %H:%M"),
					"Content-Length": len(outputdata),
					"Keep-Alive": "timeout=%d,max=%d" %(10,100),
					"Connection": "Keep-Alive",
					"Content-Type": "text/html"
				}
				
				following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
				print "following_header:", following_header
				connectionSocket.send("%s\r\n%s\r\n\r\n" %(first_header, following_header))

				# connectionSocket.send("\r\n")
				 # Date: %s\r\nKeep-Alive: timeout=10, max=100\r\n Connection: nKeep-Alive\r\n Content-Type: text/html;charset= utf-8" %(now.strftime("%Y-%m-%d %H:%m")))
				#Send the content of the requested file to the client
				for i in range(0, len(outputdata)):
					connectionSocket.send(outputdata[i])
			except IOError:
				#Send response message for file not found
				connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
				# Content-Type:text/html\r\n\r\n<!doctype html><html><body><h1>404 Not Found<h1></body></html>
				#Close client socket 

if __name__ == '__main__':
	serverSocket = socket(AF_INET, SOCK_STREAM) #Prepare a sever socket
	serverPort = 6789
	serverSocket.bind(('',serverPort))
	serverSocket.listen(5)
	threads=[]
	while True:
		#Establish the connection
		print 'Ready to serve...'
		connectionSocket, addr = serverSocket.accept()
		print "addr:\n", addr
		client_thread = ClientThread(connectionSocket,addr)
		client_thread.start()
		client_thread.setDaemon(True)
		threads.append(client_thread)
	#main thread wait all threads finish then close the connection
	"""
	# for thread in threads:
	# 	thread.join()
	If I put this, Chrome will not gonna work, safari will work.
	"""
	serverSocket.close()
