from socket import *

server_port = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('0.0.0.0', server_port))
print("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    message = message.decode()
    print(len(message), message)
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)