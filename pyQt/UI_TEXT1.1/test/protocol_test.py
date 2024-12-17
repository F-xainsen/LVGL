import struct
import sys

sys.path.append('..')

from common.protocol import *
from common.utils import *

if __name__ == '__main__':
    data = pack_protocol_data(0xE1, 2.3, 3.4, 4.5)
    # data转换为16进制字符串
    print(decode_to_hex_str(data))
    
    data = pack_protocol_data(0xF2, 5, 15, 255)
    # data转换为16进制字符串
    print(decode_to_hex_str(data))
    
    
    # 声明一个单字节的param_type为0xCC
    # param_type = bytes([0xCC])
    param_type = b'\xCC'
    print(param_type, type(param_type))
    data = pack_protocol_data_with_checksum(0xF2, param_type, 5, 15, 255)
    # data转换为16进制字符串
    print(decode_to_hex_str(data))

    # data = pack_protocol_data_with_checksum(0xE0, b'\x02', 12.345)
    data = pack_protocol_data_with_checksum(0xE0, bytes([0x02]), 12.345)
    # data转换为16进制字符串
    print(decode_to_hex_str(data))