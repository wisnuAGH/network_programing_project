# traceroute_lib/udp.py
import socket


def send_udp_packet(self, ttl):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, self.udp_protocol)
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    destination_address = socket.gethostbyname(self.destination)
    udp_socket.sendto(b'', (destination_address, 33434))
    udp_socket.close()
