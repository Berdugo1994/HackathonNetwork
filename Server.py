import socket
import time
import struct
from _thread import *
from MyUtils import Utils as utils


class Server:
    """
    Every game initiate a new server object.
    ensures all temporary memory is deleted and initiated again.
    """

    def __init__(self):
        self.groups = {
            1: [],
            2: []
        }
        self.game_on = False
        self.clients_sockets_list = []
        self.group_one = []
        self.one_team_score = 0
        self.two_team_score = 0
        self.num_of_users_at_one = 0
        self.num_of_users_at_two = 0
        tcp_master_socket = self.create_master_socket()
        start_new_thread(self.new_client_handler, (tcp_master_socket,))
        self.server_connection_udp()

    def create_master_socket(self):
        """
        creates a master socket, that will recieve all clients request to connect.
        @return: master socket.
        """
        tcp_master_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        tcp_master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        tcp_master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_master_socket.bind(
            (utils.server_ip.value, utils.tcp_server_master_port.value))
        tcp_master_socket.listen(1)
        return tcp_master_socket

    def new_client_handler(self, tcp_master_socket):
        """
        listens to tcp requests.
        creates for each tcp request his own thread.
        @param tcp_master_socket: socket of master tcp.
        """
        while True:
            """
            a loop without busy wait because accept stuck the code until receive request!
            """
            time.sleep(0.1)
            # establish connection with client
            c, addr = tcp_master_socket.accept()
            print('Connected to :', addr[0], ':', addr[1])
            # Start a new thread and return its identifier
            self.clients_sockets_list.append(c)
            start_new_thread(self.client_msg_handler, (c,))

    def server_connection_udp(self):
        """
        server sending udp broadcast
        """
        self.game_on = False
        udp_server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_server_socket.bind(('', utils.server_static_port.value))
        print("​Server started, listening on IP address " +
              str(utils.server_ip.value))
        message = struct.pack('Ibh', utils.magic_cookie.value,
                              utils.offer_message.value, utils.tcp_server_master_port.value)
        count = 0
        # counts 10 seconds until starts
        while count < 10:
            udp_server_socket.sendto(
                message, (utils.udp_ip.value, utils.udp_port.value))
            time.sleep(1)
            count += 1
        welcome_message = utils.OKBLUE.value + \
            "Welcome to Keyboard Spamming Battle Royale.\n"
        for k in self.groups.keys():
            welcome_message += 'Group' + str(k) + ":\n==\n"
            for team in self.groups[k]:
                welcome_message += team[0]+'\n'
            welcome_message += '\n\n'
        welcome_message += "Start pressing keys on your keyboard as fast as you can!!\n"
        welcome_message += "Time Started !! 10 sec lets go\n"+utils.ENDC.value
        self.send_all_clients_message(welcome_message)
        self.game_on = True
        time.sleep(10)
        finish_message = utils.OKCYAN.value + "Game over!\n"
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
                finish_message += str(team[0])+'\n'+utils.ENDC.value
        self.send_all_clients_message(finish_message)
        time.sleep(1)
        self.finish_game()
        udp_server_socket.close()
    #print_lock = threading.Lock()

    def score_update(self, c):
        """
        updating the results when client send a char.
        checks to what group does c(client) belongs and ++ their results.
        c - is connection , represnt client who plays the game.
        """
        if self.game_on:
            group_one = []
            for tup in self.groups[1]:
                group_one.append(tup[1])
            if c in self.group_one:
                self.one_team_score += 1
            else:
                self.two_team_score += 1

    def send_all_clients_message(self, message):
        """
        Send a message to all participants in this game.
        """
        for c in self.clients_sockets_list:
            c.send(bytes(message, 'utf-8'))

    def client_msg_handler(self, c):
        """
        Thread function.
        each client-socket runs this func.
        if game is not playing than the client sends his name.
        else - the client send chars !
        """
        while True:
            time.sleep(0.1)
            # data received from client
            data = c.recv(utils.buffer_size.value)
            str_data = data.decode("utf-8")
            if not self.game_on:
                # Game not started yet so each msg is first! team name msg.
                team_name = str_data
                if self.num_of_users_at_one <= self.num_of_users_at_two:
                    group = 1
                    self.num_of_users_at_one += 1
                    self.group_one.append(c)
                else:
                    group = 2
                    self.num_of_users_at_two += 1
                self.groups[group].append((team_name, c))
            elif self.game_on:
                # Game started so each msg is char! updating score.
                self.score_update(c)

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


if __name__ == '__main__':
    while True:
        time.sleep(0.5)
        server = Server()
        time.sleep(1)
