import enum
from _socket import gethostbyname, gethostname

from scapy.arch import get_if_addr


class Utils(enum.Enum):
    # Client use:
    # for local network run only, not for ssh.
    local_network_ip = gethostbyname(gethostname())
    udp_ip = '172.1.255.255'  # convention ip for udp_ip broadcasting.
    udp_port = 13117
    buffer_size = 1024
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    server_static_port = 2557
    tcp_server_master_port = 7503
    server_ip = get_if_addr('eth1')
    magic_cookie = 0xfeedbeef
    offer_message = 0x2
