import random

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
    print("​Server started, listening on IP address " + str(localIP))

    message = struct.pack('Ibh', magic_cookie, offer_message, TCP_server_master_port)
    count = 0
    while count < 10:
        udp_server_socket.sendto(message, ('255.255.255.255', UDP_port))
        time.sleep(1)
        count += 1

    # TODO: check work
    game_on = True

    welcome_message = "Welcome to Keyboard Spamming Battle Royale.\n"
    for k in groups.keys():
        welcome_message += 'Group' + str(k) + ":\n==\n"
        for team in groups[k]:
            welcome_message += team[0]

    welcome_message += "Start pressing keys on your keyboard as fast as you can!!"
    send_welcome_messages(tcp_master_socket, welcome_message)


def server_tcp():
    tcp_server_master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_master_socket.bind((localIP, TCP_server_master_port))
    tcp_server_master_socket.listen(1)
    return tcp_server_master_socket

# TODO: can delete?
print_lock = threading.Lock()


def send_welcome_messages(tcp_master_socket, message):
    for c in clients_sockets_list:
        c.send(bytes(message, 'utf-8'))

# thread function
def tcp_client_connection(c):
    while True:

        # data received from client
        data = c.recv(1024)
        str_data = data.decode("utf-8")

        if not game_on and '\n' in str_data:
            team_name = str_data
            group = random.randint(1, 2)
            groups[group].append((team_name, c))
        elif game_on:
            x = ""
        #     Start counting

        elif not data:
            print('Bye')
            break

    c.close()


def listen_tcp(tcp_master_socket):
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = tcp_master_socket.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        clients_sockets_list.append(c)
        start_new_thread(tcp_client_connection, (c,))
    tcp_master_socket.close()


if __name__ == '__main__':
    # localIP = get_if_addr('eth1')
    game_on = False
    groups = {
        1: [],
        2: []
    }
    localIP = 'localhost'
    UDP_port = 13117
    bufferSize = 1024
    server_static_port = 2057
    TCP_server_master_port = 2058
    tcp_master_socket = server_tcp()
    start_new_thread(listen_tcp, (tcp_master_socket,))
    clients_sockets_list = []
    magic_cookie = 0xfeedbeef
    offer_message = 0x2
    server_connection_UDP()
    while True:
        x = 1



