# ICMP
import socket
import struct


def send_icmp_packet(self, ttl):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.icmp_protocol)
    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    icmp_header = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
    icmp_checksum = self.calculate_checksum(icmp_header)

    icmp_packet = struct.pack('!BBHHH', 8, 0, icmp_checksum, 0, 0)

    destination_address = socket.gethostbyname(self.destination)
    icmp_socket.sendto(icmp_packet, (destination_address, 1))
    icmp_socket.close()
