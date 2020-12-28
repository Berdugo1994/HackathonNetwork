from scapy.all import get_if_addr
import socket
localIP = get_if_addr('eth1')
localPort = 13117
bufferSize = 1024
# msgFromServer = "Hello UDP Client"
#bytesToSend  = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
# UDPServerSocket.setsockopt(socket.SOL_SOCKET,socket.INADDR_BROADCAST,1)
# Bind to address and ip
UDPServerSocket.bind((localIP, 2057))
print("UDP server up and listening")
message = b"your very important message"
# Listen for incoming datagrams
count =0
while(count<1000):
    count=0
    while(count<100):
        UDPServerSocket.sendto(message, ('255.255.255.255', localPort))
        # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        # message = bytesAddressPair[0]
        # address = bytesAddressPair[1]
        # clientMsg = f"Message from Client:{message}"
        # clientIP  = f"Client IP Address:{address}"
        # print(clientMsg)
        # print(clientIP)
        count=count + 1 
        print("message")

   

    # Sending a reply to client

    # UDPServerSocket.sendto(bytesToSend, address)