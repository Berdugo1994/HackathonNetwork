from socket import *
from scapy.all import get_if_addr
import struct


def listening_to_server_udp():
    UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
    UDPclientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # UDPclientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT,1)
    UDPclientSocket.bind((serverName, server_udp_port))
    print("Client started, listening for offer requests...​")
    while (True):
        server_msg, serverAdress = UDPclientSocket.recvfrom(2048)  # Wait for message from udp
        print("Received offer from " + str(serverAdress[0]) + ", attempting to connect...")
        server_package = struct.unpack('Ibh', server_msg)
        if len(server_package) == 3 and server_package[0] == magic_cookie and server_package[1] == offer_message:
            server_tcp_port = server_package[2]
            break

    client_socket = client_tcp_network_with_server(serverAdress[0], server_tcp_port)
    listen_tcp(client_socket)


def client_tcp_network_with_server(cur_server_ip, cur_server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((cur_server_ip, cur_server_port))
    client_socket.send(TeamName)
    return client_socket


def listen_tcp(socket):
    while True:
        # data received from client
        data = socket.recv(1024)
        print(data.decode("utf-8"))

#         TODO: send back letters

### CLIENT UDP
if __name__ == '__main__':
    # localIP = get_if_addr('eth1')
    # serverName = '0.0.0.0'
    serverName = 'localhost'
    server_udp_port = 13117
    TeamName = b'EdenAndSarit\n'
    print("TEST")
    magic_cookie = 0xfeedbeef
    offer_message = 0x2
    listening_to_server_udp()