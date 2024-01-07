# UDP

import socket
import struct
from .common import calculate_checksum


def send_udp_packet(self, ttl):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, self.udp_protocol)
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    udp_header = struct.pack('!HHHH', 1234, 33434, 8, 0)
    udp_checksum = calculate_checksum(udp_header)

    udp_packet = struct.pack('!HHHH', 1234, 33434, udp_checksum)

    destination_address = socket.gethostbyname(self.destination)
    try:
        udp_socket.sendto(udp_packet, (destination_address, 33434))
    except OSError as e:
        print(f"{ttl}: {e}")
    finally:
        udp_socket.close()
