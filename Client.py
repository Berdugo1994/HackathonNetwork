from socket import *
from scapy.all import get_if_addr
import struct
import sys
import select
import time
import traceback
import os


class Client:
    def __init__(self):
        self.serverName = gethostbyname(gethostname())
        self.localIP = get_if_addr('eth1')
        self.client_socket = None
        self.serverName = '172.1.255.255'
        self.server_udp_port = 13120
        self.TeamName = b'EdenAndSarit'
        self.magic_cookie = 0xfeedbeef
        self.offer_message = 0x2
        self.server_tcp_port = None
        self.game_started = False

    def listening_to_server_udp(self):
        """
        this function listening to the UDP port amd waiting to get servers offers  
        """
        UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
        UDPclientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        UDPclientSocket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        UDPclientSocket.bind((self.serverName, self.server_udp_port))
        print("Client started, listening for offer requests...​")
        while (True):
            try:
                time.sleep(0.1)
                server_msg, serverAdress = UDPclientSocket.recvfrom(
                    2048)  # Wait for message from udp
                print("Received offer from " +
                      str(serverAdress[0]) + ", attempting to connect...")
                # unpack the server message
                server_package = struct.unpack('Ibh', server_msg)
                print("unpacked")
                # check if all packet format is correct
                if len(server_package) == 3 and server_package[0] == self.magic_cookie and server_package[
                        1] == self.offer_message:
                    self.server_tcp_port = server_package[2]
                    print("tcp_port", str(self.server_tcp_port))
                    # establish a tcp connection with the server
                    self.client_socket = self.client_tcp_network_with_server(
                        serverAdress[0], self.server_tcp_port)
                    print("netwithserver")
                    break
            except:
                traceback.print_exc()

    def start_sending_chars(self):
        """
        in this function this function the user start press on keyboard.
        """
        try:
            msg_from_server = self.client_socket.recv(1024)
            self.got_message_from_server(msg_from_server)
            self.client_socket.setblocking(0)
            os.system("stty raw -echo")
            # start playing
            while self.game_started:
                time.sleep(0.1)
                the_data = isData()
                if the_data and self.game_started:
                    c = sys.stdin.read(1)
                    self.client_socket.send(c.encode())
                try:
                    # check for messages from the server
                    msg_from_server = self.client_socket.recv(1024)
                    self.got_message_from_server(msg_from_server)
                    if not self.game_started or msg_from_server:
                        break
                except:
                    pass
            os.system("stty -raw echo")
            # returns to wait if not recv message at socket
            self.client_socket.setblocking(1)
        except:
            pass

    def client_tcp_network_with_server(self, cur_server_ip, cur_server_port):
        """
        establish tp connection with the server
        """
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect((cur_server_ip, cur_server_port))
            self.client_socket.send(self.TeamName)
            return self.client_socket
        except:
            traceback.print_exc()

    def got_message_from_server(self, server_msg):
        """
        handles message from server.
        prints and change game status.
        """
        os.system("stty -raw echo")
        print(server_msg.decode("utf-8"))
        if not self.game_started:
            self.game_started = True
            return
        if self.game_started:
            self.game_started = False
        return


def isData():
    """
    checks if the stdin loaded with chars
    """
    the_data, a, b = select.select([sys.stdin], [], [], 0)
    return the_data


# CLIENT UDP
if __name__ == '__main__':
    try:
        while True:
            time.sleep(0.1)
            client = Client()
            client.listening_to_server_udp()
            # Got server-client tcp connection
            client.start_sending_chars()
            print("finished game..")
            time.sleep(5)
    except:
        time.sleep(1)
        traceback.print_exc()
