# TCP

import socket
import struct
from .common import calculate_checksum


def send_tcp_packet(self, ttl):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, self.tcp_protocol)
    tcp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))

    tcp_header = struct.pack('!HHIIBBHHH', 1234, 80, 0, 0, 5 << 4, 0, 8192, 0, 0)
    tcp_checksum = calculate_checksum(tcp_header)

    tcp_packet = struct.pack('!HHIIBBHHH', 1234, 80, 0, 0, 5 << 4, 0, 8192, tcp_checksum, 0)

    destination_address = socket.gethostbyname(self.destination)
    try:
        tcp_socket.connect((destination_address, 80))
        tcp_socket.send(tcp_packet)
    except OSError as e:
        print(f"{ttl}: {e}")
    finally:
        tcp_socket.close()
