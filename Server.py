from scapy.all import get_if_addr
import socket
import time
import struct
from _thread import *
import threading
def server_connection_UDP():
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_server_socket.bind((localIP, server_static_port))
    print("​Server started, listening on IP address" + str(localIP))
    message = struct.pack('Ibh', 0xfeedbeef, 0x2, UDP_port)
    count = 0
    while count < 1000:
        time.sleep(1)
        count = 0
        while count < 100:
            udp_server_socket.sendto(message, ('255.255.255.255', UDP_port))
            time.sleep(1)
            establish_tcp_connection()
            count = count + 1


def server_tcp():
    tcp_server_master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_master_socket.bind((localIP, TCP_server_master_port))
    tcp_server_master_socket.listen(1)
    return tcp_server_master_socket


def establish_tcp_connection():
    connection_socket, client_address = tcp_master_socket.accept()
    sockets_list.append(connection_socket)
    msg_from_client = connection_socket.recv(1024)


if __name__ == '__main__':
    #localIP = get_if_addr('eth1')
    localIP = 'localhost'
    UDP_port = 13117
    bufferSize = 1024
    server_static_port = 2057
    TCP_server_master_port = 2058
    tcp_master_socket = server_tcp()
    server_connection_UDP()
    sockets_list = []
