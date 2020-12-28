from socket import *
from scapy.all import get_if_addr
import struct
def listening_to_server_udp():
    UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
    UDPclientSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    #UDPclientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT,1)
    UDPclientSocket.bind((serverName,serverPort))
    print("Client started, listening for offer requests...​")
    while (True):
        server_msg, serverAdress = UDPclientSocket.recvfrom(2048) #Wait for message from udp
        print("Recieved offer from " + str(serverAdress) + ", attempting to connect...")
        server_port = struct.unpack('0xfeedbeef', server_msg)
        print(server_port)

def client_tcp_network_with_server(cur_server_ip, cur_server_port):
    client_socket = socket(AF_INET,SOCK_STREAM)
    client_socket.connect((cur_server_ip, cur_server_port))
    client_socket.send(b'client says -> tcp connection succeed')







### CLIENT UDP
if __name__=='__main__':
    #localIP = get_if_addr('eth1')
    # serverName = '0.0.0.0'
    serverName= 'localhost'
    serverPort = 13117
    TeamName = b'EdenAndSarit\n'
    print("TEST")
    listening_to_server_udp()
