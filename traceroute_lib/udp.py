# UDP

import socket
import struct
from .common import calculate_checksum


def send_udp_packet(ttl, destination, udp_protocol):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp_protocol)
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    udp_source_port = 1234
    udp_destination_port = 33434

    udp_header = struct.pack('!HHHH', udp_source_port, udp_destination_port, 0, 0)
    udp_checksum = calculate_checksum(udp_header)

    udp_packet = struct.pack('!HHHH', udp_source_port, udp_destination_port, udp_checksum, 0)

    destination_address = socket.gethostbyname(destination)
    try:
        udp_socket.sendto(udp_packet, (destination_address, udp_destination_port))
    except OSError as e:
        print(f"{ttl}: {e}")
    finally:
        udp_socket.close()
