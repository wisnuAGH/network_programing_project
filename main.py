# Network programming Project AGH university
# authors: Paweł Harmata, Łukasz Żądło, Mikołaj Wiśniewski
# traceroute_lib implementation

from traceroute_lib import TracePath

destination_host = "example.com"

tracer = TracePath(destination_host)

print("Tracing route using ICMP:")
tracer.trace(protocol='icmp')

print("\nTracing route using UDP:")
tracer.trace(protocol='udp')

print("\nTracing route using TCP:")
tracer.trace(protocol='tcp')
