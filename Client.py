# from socket import *
# from getch import _Getch
# from scapy.all import get_if_addr
# #TESTSSH
# ip = get_if_addr('eth1')
# print(ip)
# serverIpOfBroadcast = '0.0.0.0'
# serverPort = 13117
# TeamName = b'EdenAndSarit\n'
# clientSocket = socket(AF_INET, SOCK_DGRAM)
# # clientSocket.connect((serverIpOfBroadcast, serverPort))
# while (True):
#     # getch = _Getch()
#     # clientSocket.send(getch)
#     #input_char = msvcrt.getch()
#     # clientSocket.send(TeamName)
#     modifiedSenetence = clientSocket.recv(1024)
#     print(modifiedSenetence)
#     if TeamName == '`':  # For Testing
#         clientSocket.close()
#         break

from socket import *
from scapy.all import get_if_addr
### CLIENT UDP 
localIP = get_if_addr('eth1')
print(localIP)
serverName = '0.0.0.0'
serverPort = 13117
TeamName = b'EdenAndSarit\n'
UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
UDPclientSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
UDPclientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT,1)
UDPclientSocket.bind((serverName,serverPort))
print("WAS HERE")
# UDPclientSocket.bind((serverName,serverPort))
message=b"TTTTTTTTesTTTTTTTTTTTT"
while (True):
    # UDPclientSocket.sendto(message,(serverName,serverPort))
    modifiedSenetence, serverAdress = UDPclientSocket.recvfrom(2048) #Wait for message from udp
    print(modifiedSenetence)
    print(serverAdress)
    # modifiedSenetence = clientSocket.recv(1024)
    # if TeamName == '`':  # For Testing
    #     clientSocket.close()
    #     break