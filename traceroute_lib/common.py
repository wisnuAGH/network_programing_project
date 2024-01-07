# Calculate checksum

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i + 1]

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16
    return ~checksum & 0xffff
