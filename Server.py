import random
from scapy.all import get_if_addr
import socket
import time
import struct
from _thread import *
import threading


class Server:
    """
    Every game initiate a new server object.
    ensures all temporary memory is deleted and initiated again.
    """

    def __init__(self):
        self.localIP = get_if_addr('eth1')
        self.groups = {
            1: [],
            2: []
        }
        self.game_on = False
        self.UDP_port = 13120
        self.bufferSize = 1024
        self.server_static_port = 2557
        self.TCP_server_master_port = 7503
        self.clients_sockets_list = []
        self.one_team_score = 0
        self.two_team_score = 0
        self.num_of_users_at_one = 0
        self.num_of_users_at_two = 0
        self.magic_cookie = 0xfeedbeef
        self.offer_message = 0x2
        self.tcp_master_socket = self.create_server_tcp()
        start_new_thread(self.listen_tcp, (self.tcp_master_socket,))
        self.server_connection_UDP()

    def create_server_tcp(self):
        """
        create master tcp socket
        """
        tcp_server_master_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_master_socket.bind(
            (self.localIP, self.TCP_server_master_port))
        tcp_server_master_socket.listen(1)
        return tcp_server_master_socket

    def listen_tcp(self, tcp_master_socket):
        """
        server listening wait for a tcp connection
        """
        # a forever loop until client wants to exit
        while True:
            time.sleep(0.1)
            # establish connection with client
            c, addr = tcp_master_socket.accept()
            print('Connected to :', addr[0], ':', addr[1])
            # Start a new thread and return its identifier
            self.clients_sockets_list.append(c)
            start_new_thread(self.tcp_client_connection, (c,))

    def server_connection_UDP(self):
        """
        server sending udp broadcast
        """
        self.game_on = False
        udp_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_server_socket.bind(('', self.server_static_port))
        print("​Server started, listening on IP address " + str(self.localIP))
        message = struct.pack('Ibh', self.magic_cookie,
                              self.offer_message, self.TCP_server_master_port)
        count = 0
        # counts 10 seconds until starts
        while count < 10:
            udp_server_socket.sendto(
                message, ('172.1.255.255', self.UDP_port))
            time.sleep(1)
            count += 1
        welcome_message = "Welcome to Keyboard Spamming Battle Royale.\n"
        for k in self.groups.keys():
            welcome_message += 'Group' + str(k) + ":\n==\n"
            for team in self.groups[k]:
                welcome_message += team[0]
        welcome_message += "Start pressing keys on your keyboard as fast as you can!!\n"
        welcome_message += "Time Started !! 20 sec lets go\n"
        self.send_all_clients_message(welcome_message)
        self.game_on = True
        time.sleep(10)
        finish_message = "Game over!\n"
        finish_message += "Group 1 typed in "
        finish_message += str(self.one_team_score)
        finish_message += " characters. Group 2 typed in "
        finish_message += str(self.two_team_score)
        finish_message += " characters.\n"
        winner_team_num = 0
        if self.one_team_score > self.two_team_score:
            finish_message += "Group 1 wins!\n"
            winner_team_num = 1
        elif self.one_team_score == self.two_team_score:
            finish_message += "It's a draw !!!\n"
        else:
            finish_message += "Group 2 wins!\n\n"
            winner_team_num = 2
        if winner_team_num != 0:
            finish_message += "Congratulations to the winners:\n==\n"
            for team in self.groups[winner_team_num]:
                finish_message += str(team[0])+'\n'
        self.send_all_clients_message(finish_message)
        time.sleep(1)
        self.finish_game()
        udp_server_socket.close()
    #print_lock = threading.Lock()

    def buffer_results(self, c):
        """
        counting results
        """
        if self.game_on:
            group_one = []
            for tup in self.groups[1]:
                group_one.append(tup[1])
            if c in group_one:
                self.one_team_score += 1
            else:
                self.two_team_score += 1

    def send_all_clients_message(self, message):
        """
        send message to all clients
        """
        for c in self.clients_sockets_list:
            c.send(bytes(message, 'utf-8'))

    def tcp_client_connection(self, c):
        """
        this is the thread function
        divide clients to groups
        """
        while True:
            time.sleep(0.1)
            # data received from client
            data = c.recv(1024)
            str_data = data.decode("utf-8")
            if not self.game_on and '\n' in str_data:
                team_name = str_data
                if self.num_of_users_at_one <= self.num_of_users_at_two:
                    group = 1
                else:
                    group = 2
                self.groups[group].append((team_name, c))
            elif self.game_on:
                self.buffer_results(c)
        c.close()

    def finish_game(self):
        """
        delete the former values belongs to last game
        """
        self.groups = {
            1: [],
            2: []
        }
        self.game_on = False
        self.clients_sockets_list = []
        self.one_team_score = 0
        self.two_team_score = 0
        self.num_of_users_at_one = 0
        self.num_of_users_at_two = 0
        self.tcp_master_socket.close()


if __name__ == '__main__':

    while True:
        try:
            time.sleep(0.1)
            server = Server()
            time.sleep(1)
        except:
            pass
