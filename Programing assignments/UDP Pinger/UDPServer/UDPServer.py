import random  
from socket import * 

serverSocket = socket(AF_INET, SOCK_DGRAM)  # Crea socket udp para el servidor
serverSocket.bind(('10.0.0.2', 4000))  # Direcion ip y puerto
print("Server Running...") 
while True: 
    rand = random.randint(0, 10)  # simulando perdida de paquetes
    message, address = serverSocket.recvfrom(1024)
    message = message.upper()  
    if rand < 6:  # < 60% de perdida
        continue
    serverSocket.sendto(message, address)  # Mandar el mensaje de vuelta al cliente
