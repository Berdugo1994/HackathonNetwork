import random
from scapy.all import get_if_addr
import socket
import time
import struct
from _thread import *
import threading




class Server:



    def __init__(self):
        # localIP = get_if_addr('eth1')
        self.groups = {
            1: [],
            2: []
        }
        self.game_on = False
        # localIP = 'localhost'
        self.localIP = socket.gethostbyname(socket.gethostname())
        self.UDP_port = 13117
        self.bufferSize = 1024
        self.server_static_port = 2057
        self.TCP_server_master_port = 2058
        self.clients_sockets_list = []
        self.magic_cookie = 0xfeedbeef
        self.offer_message = 0x2
        self.one_team_score=0
        self.two_team_score=0
        self.tcp_master_socket = self.server_tcp()
        start_new_thread(self.listen_tcp, (self.tcp_master_socket,))
        self.server_connection_UDP()


    def server_tcp(self):
        tcp_server_master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_master_socket.bind((self.localIP, self.TCP_server_master_port))
        tcp_server_master_socket.listen(1)
        return tcp_server_master_socket

    def server_connection_UDP(self):
        self.game_on=False
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_server_socket.bind((self.localIP, self.server_static_port))
        print("​Server started, listening on IP address " + str(self.localIP))
        message = struct.pack('Ibh', self.magic_cookie, self.offer_message, self.TCP_server_master_port)
        count = 0
        # TODO change to while count < 10:
        while count < 10:
            udp_server_socket.sendto(message, ('255.255.255.255', self.UDP_port))
            time.sleep(1)
            count += 1
        # TODO: check work
        welcome_message = "Welcome to Keyboard Spamming Battle Royale.\n"
        for k in self.groups.keys():
            welcome_message += 'Group' + str(k) + ":\n==\n"
            for team in self.groups[k]:
                welcome_message += team[0]
        welcome_message += "Start pressing keys on your keyboard as fast as you can!!\n"
        welcome_message += "Time Started !! 20 sec lets go\n"
        time.sleep(5)  # let players into the game
        self.send_all_clients_message(self.tcp_master_socket, welcome_message)
        print("Game started")
        self.game_on = True
        time.sleep(30)
        print("And the winner is team")
        if self.one_team_score>self.two_team_score:
            print("1")
        elif self.one_team_score == self.two_team_score:
            print("equals")
        else:
            print("2")
        self.send_all_clients_message(self.tcp_master_socket, "ServerStopped")
        time.sleep(3)




    # TODO: can delete?
    print_lock = threading.Lock()

    def buffer_results(self,c):
        if self.game_on:
            group_one = []
            for tup in self.groups[1]:
                group_one.append( tup[1])
            if c in group_one:
                self.one_team_score += 1
            else:
                self.two_team_score += 1

    #     Start counting


    def send_all_clients_message(self,tcp_master_socket, message):
        for c in self.clients_sockets_list:
            c.send(bytes(message, 'utf-8'))



    # thread function
    def tcp_client_connection(self,c):
        while True:
            # data received from client
            data = c.recv(1024)
            str_data = data.decode("utf-8")
            print(str_data)
            if not self.game_on and '\n' in str_data:
                team_name = str_data
                group = random.randint(1, 2)
                self.groups[group].append((team_name, c))

            elif self.game_on:
                self.buffer_results(c)


            elif not data:
                print('Bye')
                break

        c.close()


    def listen_tcp(self,tcp_master_socket):
        # a forever loop until client wants to exit
        while True:
            # establish connection with client
            c, addr = tcp_master_socket.accept()

            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            self.clients_sockets_list.append(c)
            start_new_thread(self.tcp_client_connection, (c,))
        tcp_master_socket.close()


if __name__ == '__main__':
    server = Server()
