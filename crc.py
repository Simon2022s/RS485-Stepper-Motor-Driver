# crc16
def calc_crc(string):
    data = bytearray.fromhex(string)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    # hex_crc = hex(((crc & 0xff) << 8) + (crc >> 8))
    crc_0 = crc & 0xff
    crc_1 = crc >> 8
    str_crc_0 = '{:02x}'.format(crc_0).upper()
    str_crc_1 = '{:02x}'.format(crc_1).upper()
    return str_crc_0 + str_crc_1


