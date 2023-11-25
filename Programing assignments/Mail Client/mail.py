from socket import *
import base64
import ssl

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
mailFromAddress = input('Insert your email(it has to be from Gmail): ')
mailPassWord = input('Insert your gmail app password')
mailToAddress = input('Insert the email that is going to receive the message')

msg = 'FROM: ' + mailFromAddress + '\r\n'
msg += 'TO: ' + mailToAddress +  '\r\n'
msg += 'Subject: ' + 'test' +  '\r\n'
msg += "\r\n I love computer networks2!"
endmsg = "\r\n.\r\n"

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 465)) # El puerto 587 se usa con TLS

context = ssl.create_default_context() # Esta linea es opcional, es para añadir SSL
clientSocketSSL = context.wrap_socket(clientSocket, server_hostname=mailserver) # Esta linea es opcional, es para añadir SSL

# En caso de no usar SSL se debe usar la variable clientSocket en vez de clientSocketSSL
recv = clientSocketSSL.recv(1024)
recv = recv.decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO mailserver\r\n'
clientSocketSSL.send(heloCommand.encode())
recv1 = clientSocketSSL.recv(1024)
recv1 = recv1.decode()
print(recv1)


# Login
loginCommand = 'AUTH LOGIN\r\n'
clientSocketSSL.send(loginCommand.encode())
recv2 = clientSocketSSL.recv(1024)
recv2 = recv2.decode()
print('auth login')
print(recv2)


# send base64 encrypted username
print(mailFromAddress)
userCommand = base64.b64encode(mailFromAddress.encode()).decode() + '\r\n'
clientSocketSSL.send(userCommand.encode())
recv3 = clientSocketSSL.recv(1024)
recv3 = recv3.decode()
print(recv3)


# send base64 encrypted password
print(mailPassWord)
passCommand = base64.b64encode(mailPassWord.encode()).decode() + '\r\n'
clientSocketSSL.send(passCommand.encode())
recv4 = clientSocketSSL.recv(1024)
recv4 = recv4.decode()
print(recv4)

# Send MAIL FROM command and print server response.
MFCommand = f'MAIL FROM: <{mailFromAddress}>\r\n'
clientSocketSSL.send(MFCommand.encode())
recv5 = clientSocketSSL.recv(1024)
recv5 = recv5.decode()
print(recv5)

# Send RCPT TO command and print server response.
RTCommand = f'RCPT TO: <{mailToAddress}>\r\n'
clientSocketSSL.send(RTCommand.encode())
recv6 = clientSocketSSL.recv(1024)
recv6 = recv6.decode()
print(recv6)

# Send DATA command and print server response.
DATACommand = 'DATA\r\n'
clientSocketSSL.send(DATACommand.encode())
recv7 = clientSocketSSL.recv(1024)
recv7 = recv7.decode()
print(recv7)

# Send message data.
clientSocketSSL.send(msg.encode())

# Message ends with a single period.
clientSocketSSL.send(endmsg.encode())
recv8 = clientSocketSSL.recv(1024)
recv8 = recv8.decode()
print(recv8)

# Send QUIT command and get server response.
QUITCommand = 'QUIT\r\n'
clientSocketSSL.send(QUITCommand.encode())
recv9 = clientSocketSSL.recv(1024)
recv9 = recv9.decode()
print(recv9)


clientSocketSSL.close()
