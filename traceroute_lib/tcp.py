# traceroute_lib/tcp.py
import socket


def send_tcp_packet(self, ttl):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, self.tcp_protocol)
    tcp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    destination_address = socket.gethostbyname(self.destination)
    tcp_socket.connect((destination_address, 80))
    tcp_socket.close()
