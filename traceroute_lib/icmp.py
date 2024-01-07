# ICMP

import socket
import struct
from .common import calculate_checksum


def send_icmp_packet(ttl, destination, icmp_protocol):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_protocol)
    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    icmp_header = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
    icmp_checksum = calculate_checksum(icmp_header)

    icmp_packet = struct.pack('!BBHHH', 8, 0, icmp_checksum, 0, 0)

    destination_address = socket.gethostbyname(destination)
    try:
        icmp_socket.sendto(icmp_packet, (destination_address, 1))
    except OSError as e:
        print(f"{ttl}: {e}")
    finally:
        icmp_socket.close()
