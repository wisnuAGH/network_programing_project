# Network programming Project AGH university
# authors: Paweł Harmata, Łukasz Żądło, Mikołaj Wiśniewski
# traceroute_lib implementation

from traceroute_lib import TracePath


if __name__ == "__main__":
    destination_host = input("Enter the destination host: ")

    while True:
        print("Choose protocol: icmp, udp, tcp")
        selected_protocol = input("Enter the protocol: ")

        tracer = TracePath(destination_host)

        if selected_protocol == 'icmp':
            print("Tracing route using ICMP:")
            tracer.trace(protocol='icmp')
            break
        elif selected_protocol == 'udp':
            print("\nTracing route using UDP:")
            tracer.trace(protocol='udp')
            break
        elif selected_protocol == 'tcp':
            print("\nTracing route using TCP:")
            tracer.trace(protocol='tcp')
            break
        else:
            print("Invalid protocol!")
