# Network programming Project AGH university
# authors: Paweł Harmata, Łukasz Żądło, Mikołaj Wiśniewski

import sys
import socket
from scapy.all import *

def udp_traceroute(destination, max_hops=30, timeout=2):
    for ttl in range(1, max_hops + 1):
        packet = IP(dst=destination, ttl=ttl) / UDP(dport=33434)
        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            break
        elif reply.type == 3:  # ICMP Time Exceeded
            print(f"{ttl}: {reply.src}")
            if reply.src == destination:
                print("Destination reached!")
                break
        elif reply.type == 0:  # ICMP Echo Reply
            print(f"{ttl}: {reply.src}")
            print("Destination reached!")
            break
        else:
            print(f"{ttl}: {reply.src} - Unknown ICMP type {reply.type}")

def icmp_traceroute(destination, max_hops=30, timeout=2):
    for ttl in range(1, max_hops + 1):
        packet = IP(dst=destination, ttl=ttl) / ICMP()
        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            break
        elif reply.type == 11:  # ICMP Time Exceeded
            print(f"{ttl}: {reply.src}")
            if reply.src == destination:
                print("Destination reached!")
                break
        elif reply.type == 0:  # ICMP Echo Reply
            print(f"{ttl}: {reply.src}")
            print("Destination reached!")
            break
        else:
            print(f"{ttl}: {reply.src} - Unknown ICMP type {reply.type}")

if name == "main":
    if len(sys.argv) != 3:
        print("Usage: python traceroute.py <destination> <protocol>")
        sys.exit(1)

    destination = sys.argv[1]
    protocol = sys.argv[2].lower()

    if protocol == "udp":
        udp_traceroute(destination)
    elif protocol == "icmp":
        icmp_traceroute(destination)
    else:
        print("Invalid protocol. Supported protocols: udp, icmp")