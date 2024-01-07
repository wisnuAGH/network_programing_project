# Traceroute

import socket
import time
from .icmp import send_icmp_packet
from .udp import send_udp_packet
from .tcp import send_tcp_packet


class TracePath:
    def __init__(self, destination, max_hops=30, timeout=1):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout

    def trace(self, protocol='icmp'):
        for ttl in range(1, self.max_hops + 1):
            start_time = time.time()

            if protocol == 'icmp':
                send_icmp_packet(ttl, self.destination)
            elif protocol == 'udp':
                send_udp_packet(ttl, self.destination)
            elif protocol == 'tcp':
                send_tcp_packet(ttl, self.destination)

            receive_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            receive_socket.settimeout(self.timeout)

            try:
                _, _, _, _, addr = receive_socket.recvfrom(512)
                end_time = time.time()
                round_trip_time = (end_time - start_time) * 1000
                print(f"{ttl}: {addr[0]}, RTT: {round_trip_time:.3f} ms")
            except socket.timeout:
                print(f"{ttl}: *")

            receive_socket.close()

            if addr[0] == self.destination:
                break
