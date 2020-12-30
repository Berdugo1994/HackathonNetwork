from socket import *
from scapy.all import get_if_addr
import struct
from pynput import Key, Listener


def listening_to_server_udp():
    UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
    UDPclientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # UDPclientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT,1)
    UDPclientSocket.bind((serverName, server_udp_port))
    print("Client started, listening for offer requests...​")
    while (True):
        server_msg, serverAdress = UDPclientSocket.recvfrom(2048)
        # if serverAdress == '172.18.0.80':
        #     print("Not me")
        #     continue
        print("Received offer from ")
        print(str(serverAdress[0]))
        print(", attempting to connect...")
        try:
            server_package = struct.unpack('Ibh', server_msg)
            if len(server_package) == 3 and server_package[0] == magic_cookie and server_package[1] == offer_message:
                server_tcp_port = server_package[2]
                break
        except:
            print("bad packet from server")
    client_socket = client_tcp_network_with_server(
        serverAdress[0], server_tcp_port)
    listen_tcp(client_socket)


def client_tcp_network_with_server(cur_server_ip, cur_server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((cur_server_ip, cur_server_port))
    client_socket.send(TeamName)
    return client_socket


def on_press(key):
    print('{0} pressed'.format(
        key))


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


def listen_tcp(socket):
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    while True:
        # data received from client
        data = socket.recv(1024)
        # TODO: convert normally from bytes to string
        print(str(data))

    # while True:
    #
    #     # data received from client
    #     data = c.recv(1024) #should be welcome message
    #     print(data)


#         TODO: send back letters

# CLIENT UDP
if __name__ == '__main__':
    localIP = get_if_addr('eth1')
    serverName = '0.0.0.0'
    # serverName = 'localhost'
    server_udp_port = 13117
    TeamName = b'EdenAndSarit\n'
    print("TEST")
    # magic_cookie = 0xfeedbeef
    magic_cookie = 0xfeedbeee
    offer_message = 0x2
    listening_to_server_udp()
