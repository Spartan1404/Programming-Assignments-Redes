from socket import *
import time                 
import datetime             
from decimal import Decimal 


serverIPaddress = '10.0.0.2'   
port = 12345
n = 10                 
m = 15                

sent = 0            # initial number of packets sent
received = 0        # initial number of packets received
lost = 0            # initial number of packets lost 
minrtt = 1000000    # initial minimum RTT
avgrtt = 0          # initial average RTT
maxrtt = 0          # initial maximum RTT
ping = 1            # initial ping number
while ping <= 50:   # ping 50 times
    if ping < n or ping > m:                            # skip range of packets   
        clientSocket = socket(AF_INET, SOCK_DGRAM)      # make UDP socket
        clientSocket.settimeout(1)                      # 1 sec time out
        message = str(ping)                             # convert ping num/sequence num to string
        address = (serverIPaddress, port)               # serverIP and port num
        begin = time.time()                             # store initial time
        clientSocket.sendto(bytes(message , 'UTF-8'), address)           # send packet num to server
        sent = sent + 1                                 # increase num of pings sent
        try:
            data, server = clientSocket.recvfrom(1024)  # get data back from server
            current = time.time()                       # store current time
            dt = datetime.datetime.now()            # for printing time stamp
            RTT = current - begin               # store rtt
            if ping == 1:                   # re-initialize min, avg, and max rtts
                minrtt = RTT
                avgrtt = RTT
                maxrtt = RTT
            else:                           # keep track of min, avg, and max rtts
                avgrtt = avgrtt + RTT
                if RTT < minrtt:
                    minrtt = RTT
                if RTT > maxrtt:
                    maxrtt = RTT
            received = received + 1         # increase num of pings received
            # print and format current ping statstics
            print ("Reply from " + str(serverIPaddress) + ": PING " + str(ping) + dt.strftime(" %a %b %d %H:%M:%S %Y\n") + "RTT: " + str(RTT))
        except timeout:
            lost = lost + 1                 # increase num of pings lost
            print ("Request timed out")       # print time out msg
    ping = ping + 1                         # increase ping/sequence number
    
rate = Decimal(100.0 * lost / sent)         # calculate and store packet loss rate
rate = round(rate,1)                        # round to 1 decimal place
# print and format all ping/packets statistics
print (str(sent) + " packets sent, " + str(received) + " packets received, " + str(lost) + " packets lost, packet loss rate: " + str(rate) + " %")

avgrtt = avgrtt / received                  # finish calculating average rtt
# print and format rtt statistics
print ("minRTT = " + str(minrtt) + ", avgRTT = " + str(avgrtt) + ", maxRTT = " + str(maxrtt))

