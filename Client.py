from socket import *
from scapy.all import get_if_addr
import struct
import sys
import select
import time
import traceback
import os
from MyUtils import Utils as utils


class Client:
    def __init__(self):
        """
            constructor to a client (single game)
            team_name - a funny name with gratitude to Neta Barzilay.
            tcp_socket - a future variable holds the socket of the game.
            magic_cookie,offer_message - variable that holds hackathon protocol values.
            game_running - boolean that express the status of the game.
        """
        self.team_name = b'Nana Banana'
        self.tcp_socket = None
        self.magic_cookie = 0xfeedbeef
        self.offer_message = 0x2
        self.game_running = False

    def listening_to_server_udp(self):
        """
        this function listening to the UDP port amd waiting to get servers offers
        """
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        udp_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        udp_socket.bind((utils.udp_ip.value, utils.udp_port.value))
        print("Client started, listening for offer requests...​")
        while (True):
            """
            in this loop the client try's to create a tcp connection.
            with the ip and port he got from the server broadcast message.
            in case of bad values (for example port > 65353) the connection will fail,
            and will be catch in the except block.
            the loop is not a busy wait because the func 'recvfrom' is blocked until recieve a message from Udp Socket
            """
            try:
                time.sleep(0.1)
                server_msg, serverAdress = udp_socket.recvfrom(
                    2048)  # Wait for message from udp
                print("Received offer from " +
                      str(serverAdress[0]) + ", attempting to connect...")
                # unpacking the message from udp.
                # make sure the magic cookie is as determined by the hackathon.
                server_package = struct.unpack('Ibh', server_msg)
                if len(server_package) == 3 and server_package[0] == self.magic_cookie and server_package[
                        1] == self.offer_message:
                    server_tcp_port = server_package[2]
                    # establish a tcp connection with the server
                    self.tcp_socket = self.establish_tcp_connection(
                        serverAdress[0], server_tcp_port)
                    break  # important break, in case we 'break' means established succeed !
                    # else , will fall in except due to a bad server args, and will iterate again,until succeeds.
            except:
                print("Failed to connect ! trys again in 100ms...")

    def game_playing(self):
        """
        at this stage of flow the game is about to start in a second, at the moment we got the 'start game' message from
        the server, we will start typing.
        """
        # try:
        msg_from_server = self.tcp_socket.recv(1024)
        self.message_from_server_handler(msg_from_server)
        self.tcp_socket.setblocking(0)
        # make sure chars are not printed to screen while playing."disable echoing"
        os.system("stty raw -echo")
        # start playing
        while self.game_running:
            time.sleep(0.2)
            the_data = data_loaded()
            if the_data and self.game_running:
                c = sys.stdin.read(1)
                self.tcp_socket.send(c.encode())  # this line sends the char.
            try:
                # try catch because recv throws exception if not got message from server (set blocking set to 0)
                msg_from_server = self.tcp_socket.recv(1024)
                self.message_from_server_handler(msg_from_server)
                if not self.game_running or msg_from_server:
                    break
            except:
                pass
        os.system("stty -raw echo")
        # returns to wait if not recv message at socket
        self.tcp_socket.setblocking(1)
        # except:
        #     pass

    def establish_tcp_connection(self, cur_server_ip, cur_server_port):
        """
        @param cur_server_ip: string represent the ip address to connect
        @param cur_server_port: int number represent the port address to connect
        @return: tcp socket

        *** might throw except in case of bad values for arguments.
            will catch at the caller function : listening_to_server_udp
        """
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.connect((cur_server_ip, cur_server_port))
        self.tcp_socket.send(self.team_name)
        return self.tcp_socket

    def message_from_server_handler(self, server_msg):
        """
        @param : server_msg - string express to the message from server.
        handles message from server.
        prints and change game status.

        """
        os.system("stty -raw echo")
        print(server_msg.decode("utf-8"))
        if not self.game_running:
            self.game_running = True
            return
        if self.game_running:
            self.game_running = False


def data_loaded():
    """
    checks if the stdin loaded with chars
    return boolean status - true if loaded, false if not.
    """
    the_data, a, b = select.select([sys.stdin], [], [], 0)
    return the_data


if __name__ == '__main__':
    """
    main loop : 
    an infinity loop. each iterate describes a game.
    every loop we initiate a new 'client' every value is initiated. 
    sleep of 0.1seconds to make sure the server is not to busy.
    """
    while True:
        time.sleep(0.1)
        client = Client()
        client.listening_to_server_udp()
        # Got server-client tcp connection
        client.game_playing()
        print("finished game..")
        time.sleep(5)
