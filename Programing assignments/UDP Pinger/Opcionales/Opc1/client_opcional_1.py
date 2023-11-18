import socket
import time

while True:
    print('\nElija una opcion')
    print('---------------------------')
    print('Presione cualquier tecla para iniciar')
    print('Presione 0 para salir')
    print('----------------------------\n')

    option = input('Seleccione la opcion: ')
    if option == 0:
        break
    print('Starting ping...')
    print('------------------------\n')

    # create an udp socket for the client
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddress = ('10.0.0.2', 4000)
    mysocket.settimeout(3)
    RTT = []
    successful_pings = 0

    try:
        for i in range(0, 9):
            start = time.time()
            message = 'ping' + str(i) + '' + time.ctime(start)
            try:
                sent = mysocket.sendto(message.encode('utf-8'), serverAddress)
                print('sent' + message)
                data, server = mysocket.recvfrom(4096) #max data recieved 4096 bytes
                print('recievec' + str(data))
                end = time.time()
                elapsed = end - start
                RTT.append(elapsed)
                successful_pings += 1
                print('Time: ' + str(elapsed*1000) + 'miliseconds\n')
            except socket.timeout:
                print('#' + str(i) + 'Requested time out\n')
    finally:
    	if RTT:
   		min_rtt = min(RTT)
   		max_rtt = max(RTT)
   		avg_rtt = sum(RTT) / len(RTT)
   		packet_loss_rate = (10 - successful_pings) / 10 * 100
   		print(f'Minimum RTT: {min_rtt} seconds')
   		print(f'Maximum RTT: {max_rtt} seconds')
   		print(f'Average RTT: {avg_rtt} seconds')
  		print(f'Packet loss rate: {packet_loss_rate} %')
        print('Finishing ping, closing socket')
        mysocket.close()
