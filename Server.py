from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('THE SERVER IS RDY TO RECIEVE')
while True:
    connectionSocket, addr =serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    print("Team " + sentence + "was added to the party, welcome ")
    connectionSocket.send(b"welcome")
