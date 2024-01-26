# Traceroute

import socket
import time
from .icmp import send_icmp_packet
from .udp import send_udp_packet
from .tcp import send_tcp_packet


def translate_destination(destination):
    try:
        translated_destination = socket.gethostbyaddr(destination)[0]
    except socket.herror:
        translated_destination = destination
    return translated_destination


class TracePath:
    def __init__(self, destination, max_hops=30, timeout=1):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout
        self.icmp_protocol = socket.getprotobyname('icmp')
        self.udp_protocol = socket.getprotobyname('udp')
        self.tcp_protocol = socket.getprotobyname('tcp')

    def trace(self, protocol='icmp'):
        translated_destination = translate_destination(self.destination)
        addr = ["127.0.0.1", 0]
        for ttl in range(1, self.max_hops + 1):
            start_time = time.time()

            if protocol == 'icmp':
                send_icmp_packet(ttl, self.destination, self.icmp_protocol)
            elif protocol == 'udp':
                send_udp_packet(ttl, self.destination, self.udp_protocol)
            elif protocol == 'tcp':
                if send_tcp_packet(ttl, self.destination, self.tcp_protocol) == 1:
                    print("TCP: failed to establish connection.")
                    break

            receive_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            receive_socket.settimeout(self.timeout)

            try:
                packet, addr = receive_socket.recvfrom(512)
                end_time = time.time()
                round_trip_time = (end_time - start_time) * 1000
                print(f"{ttl}: {addr[0]}, RTT: {round_trip_time:.3f} ms")
            except socket.timeout:
                print(f"{ttl}: *")

            receive_socket.close()

            if translate_destination(addr[0]) == translated_destination:
                break
