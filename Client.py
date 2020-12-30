from socket import *
from scapy.all import get_if_addr
import struct
import sys
import select
import time
import traceback


class Client:
    def __init__(self):
        self.serverName = gethostbyname(gethostname())
        self.localIP = get_if_addr('eth1')
        self.client_socket = None
        self.serverName = '0.0.0.0'
        self.server_udp_port = 13117
        self.TeamName = b'EdenAndSarit\n'
        self.magic_cookie = "0xfeedbeef"
        self.offer_message = "0x2"
        self.server_tcp_port = None
        self.game_started = False

    def listening_to_server_udp(self):
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
                server_package = struct.unpack('Ibh', server_msg)
                if len(server_package) == 3 and hex(server_package[0]) == self.magic_cookie and hex(server_package[
                        1]) == self.offer_message:
                    if hex(server_package[2]) > "1024" and hex(server_package[2]) <= "65353":
                        self.server_tcp_port = server_package[2]
                        self.client_socket = self.client_tcp_network_with_server(
                            serverAdress[0], self.server_tcp_port)
                        break
            except:
                pass

    def start_sending_chars(self):
        os.system("stty raw -echo")
        msg_from_server = self.client_socket.recv(1024)
        self.stop_when_server_says(msg_from_server)
        self.client_socket.setblocking(0)
        while self.game_started:
            # sys.stdin.buffer.flush()
            # in case of terminal is not empty
            the_data = isData()
            if the_data and self.game_started:
                c = sys.stdin.read(1)
                self.client_socket.send(c.encode())
            try:
                msg_from_server = socket.recv(1024)
                self.stop_when_server_says(msg_from_server)
                if not self.game_started:
                    break
            except:
                pass  # not income msg from server
        # finish sending chars !
        os.system("stty -raw echo")
        # returns to wait if not recv message at socket
        self.client_socket.setblocking(1)

    def client_tcp_network_with_server(self, cur_server_ip, cur_server_port):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((cur_server_ip, cur_server_port))
        self.client_socket.send(self.TeamName)
        return self.client_socket

        """
        Every message from Server we open/ close the option to send messages
        """

    def stop_when_server_says(self, server_msg):
        if not self.game_started:
            self.game_started = True
            return
        if self.game_started:
            self.game_started = False
        return 


def isData():
    the_data, a, b = select.select([sys.stdin], [], [], 0)
    return the_data


# CLIENT UDP
if __name__ == '__main__':
    client = Client()
    client.listening_to_server_udp()
    # Got server-client tcp connection
    client.start_sending_chars()
