# Network programming Project AGH university
# authors: Paweł Harmata, Łukasz Żądło, Mikołaj Wiśniewski

import socket
import struct
import time


class TracePath:
    def __init__(self, destination, max_hops=30, timeout=1):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout
        self.icmp_protocol = socket.getprotobyname('icmp')
        self.udp_protocol = socket.getprotobyname('udp')
        self.tcp_protocol = socket.getprotobyname('tcp')

    def send_icmp_packet(self, ttl):
        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.icmp_protocol)
        icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        icmp_header = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
        icmp_checksum = self.calculate_checksum(icmp_header)

        icmp_packet = struct.pack('!BBHHH', 8, 0, icmp_checksum, 0, 0)

        destination_address = socket.gethostbyname(self.destination)
        icmp_socket.sendto(icmp_packet, (destination_address, 1))
        icmp_socket.close()

    def send_udp_packet(self, ttl):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, self.udp_protocol)
        udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        destination_address = socket.gethostbyname(self.destination)
        udp_socket.sendto(b'', (destination_address, 33434))
        udp_socket.close()

    def send_tcp_packet(self, ttl):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, self.tcp_protocol)
        tcp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        destination_address = socket.gethostbyname(self.destination)
        tcp_socket.connect((destination_address, 80))
        tcp_socket.close()

    def calculate_checksum(self, data):
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]

        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16
        return ~checksum & 0xffff

    def trace(self, protocol='icmp'):
        for ttl in range(1, self.max_hops + 1):
            start_time = time.time()

            if protocol == 'icmp':
                self.send_icmp_packet(ttl)
            elif protocol == 'udp':
                self.send_udp_packet(ttl)
            elif protocol == 'tcp':
                self.send_tcp_packet(ttl)

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


if __name__ == "__main__":
    destination_host = "example.com"

    tracer = TracePath(destination_host)

    print("Tracing route using ICMP:")
    tracer.trace(protocol='icmp')

    print("\nTracing route using UDP:")
    tracer.trace(protocol='udp')

    print("\nTracing route using TCP:")
    tracer.trace(protocol='tcp')
