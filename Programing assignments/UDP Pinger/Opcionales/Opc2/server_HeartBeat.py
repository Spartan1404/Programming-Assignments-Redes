from socket import *

serverIPaddress = '10.0.0.2'  
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIPaddress, 12345))

maxTimeOuts = 10        # holds maximum number of time outs
consecTimeOuts = 0      # initialize consecutive number of time outs
previous = 0            # holds previous sequence number, initialized to 0
while True:
    try:
        serverSocket.settimeout(1)                      # 1 sec time out
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)  
        message = int(message,base=10)                  # convert sequence num to int
        diff = message - previous                       # store difference between seq nums
        if diff > 1:                                    # if packet(s) are skipped
            print ("Lost " + str(diff - 1) + " messages") # print num of lost messages
            print ("Server received msg " + str(message)) # print current sequence num
            previous = message                          # assign current seq num to previous
            consecTimeOuts = 0                          # 0 consecutive time outs
        else:                                           # otherwise
            print ("Server received msg " + str(message)) # print current sequence num
            previous = message                          # assign current seq num to previous
            consecTimeOuts = 0                          # 0 consecutive time outs
        message = str(message)                          # convert sequence num to string
        serverSocket.sendto(bytes(message , 'UTF-8'), address)           # send data back to client    
    except timeout:
        print ("Server timed out")                        # print time out msg
        consecTimeOuts = consecTimeOuts + 1             # increase consecTimeOuts by 1
        if consecTimeOuts >= maxTimeOuts:
            print('client does not respond')
            break               # if 50 or more consecTimeOuts
            break  
