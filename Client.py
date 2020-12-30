from pynput.keyboard import Key, Listener
from socket import *
from scapy.all import get_if_addr
import struct

class Client:
    def __init__(self):
        self.serverName = gethostbyname(gethostname())
        self.client_socket=None
        # localIP = get_if_addr('eth1')
        # serverName = '0.0.0.0'
        # serverName = 'localhost'
        self.server_udp_port = 13117
        self.TeamName = b'EdenAndSarit\n'
        print("TEST")
        self.magic_cookie = 0xfeedbeef
        self.offer_message = 0x2
        self.server_tcp_port=None


    def listening_to_server_udp(self):
        UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
        UDPclientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # UDPclientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT,1)
        UDPclientSocket.bind((self.serverName, self.server_udp_port))
        print("Client started, listening for offer requests...​")
        while (True):
            server_msg, serverAdress = UDPclientSocket.recvfrom(2048)  # Wait for message from udp
            print("Received offer from " + str(serverAdress[0]) + ", attempting to connect...")
            server_package = struct.unpack('Ibh', server_msg)
            if len(server_package) == 3 and server_package[0] == self.magic_cookie and server_package[1] == self.offer_message:
                self.server_tcp_port = server_package[2]
                break

        self.client_socket = self.client_tcp_network_with_server(serverAdress[0], self.server_tcp_port)
        self.listen_tcp(self.client_socket)


    def client_tcp_network_with_server(self,cur_server_ip, cur_server_port):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((cur_server_ip, cur_server_port))
        client_socket.send(self.TeamName)
        return client_socket


    def listen_tcp(self,socket):
        lam_onpress = lambda key: self.on_press(key)
        lam_swss = lambda key: self.stop_when_server_says(key)
        listener = Listener(
            on_press=lam_onpress,
            on_release=lam_swss)
        listener.start()
        res = True
        while res:
            data = socket.recv(1024)
            print(data.decode("utf-8"))
    #         TODO: send back letters
            res = self.stop_when_server_says(data)
        print("client finished")

    def on_press(self,key):
        print('{0} pressed'.format(
            key))
        self.client_socket.send(b't')

    def stop_when_server_says(self,server_msg):
        print(server_msg)
        if server_msg == "ServerStopped":
            # Stop listener
            return False
        return True


### CLIENT UDP
if __name__ == '__main__':
    client = Client()
    client.listening_to_server_udp()
    listening_to_server_udp()

