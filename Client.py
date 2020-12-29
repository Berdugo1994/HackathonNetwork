from socket import *
from scapy.all import get_if_addr
import struct


def listening_to_server_udp():
    UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
    UDPclientSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    UDPclientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT,1)
    UDPclientSocket.bind((serverName,serverPort))
    print("Client started, listening for offer requests...​")
    while (True):
        # UDPclientSocket.sendto(message,(serverName,serverPort))
        server_msg, serverAdress = UDPclientSocket.recvfrom(2048) #Wait for message from udp
        print("Recieved offer from " + str(serverAdress) + ", attempting to connect...")
        server_port = struct.unpack('Ibh', server_msg)
        if len(server_port)>6:
            continue
        # modifiedSenetence = clientSocket.recv(1024)
        # if TeamName == '`':  # For Testing
        #     clientSocket.close()
        #     break


### CLIENT UDP 
if __name__=='__main__':
    localIP = get_if_addr('eth1')
    serverName = '0.0.0.0'
    serverPort = 13117
    TeamName = b'EdenAndSarit\n'
    print("TEST")
    listening_to_server_udp()