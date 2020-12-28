from socket import *
from getch import _Getch
#TESTSSH
hello="SSSSS"
serverName = 'localhost'
serverPort = 12000
TeamName = b'EdenAndSarit\n'
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while (True):
    # getch = _Getch()
    # clientSocket.send(getch)
    #input_char = msvcrt.getch()
    clientSocket.send(TeamName)
    # modifiedSenetence = clientSocket.recv(1024)
    if TeamName == '`':  # For Testing
        clientSocket.close()
        break
