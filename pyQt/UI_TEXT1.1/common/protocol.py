import struct

def decode_to_hex_str(data: bytes):
    # 将hex字符串转成大写，每两个字符用空格分隔
    data_hex = data.hex().upper()
    data_hex = " ".join([data_hex[i:i + 2] for i in range(0, len(data_hex), 2)])
    return data_hex

        
def hex2str(data, with_space=True, with_0x=True):
    """ Convert hex data to string

    Example:
    input: [255,227,2]
    output: "0xFF 0xE3 2"
    
    input: 255
    output: "0xFF"

    :param data: 数字或列表
    :param with_space: 是否带空格
    :param with_0x: 是否带0x
    """
    spliter = " " if with_space else ""
    prefix = "0x" if with_0x else ""
    if type(data) == int:
        rst = hex(data)
        if not with_0x:
            rst = rst[2:]
        return rst
    
    return spliter.join([f"{prefix}{i:02X}" for i in data])
    
def str2hex(data_str: str):
    """ Convert string to hex data
    inut:
    0xFF 0xE3 0x2
    FF E3 2
    FF E3 02
    FFE302
    
    output:
    [0xFF, 0xE3, 0x2]
    
    :param data: 字符串
    :return: 十六进制数据 [0xFF, 0xE3, 0x2]
    """
    # 移除所有0x
    data_str = data_str.replace("0x", "")
    # 如果有的数字是单个的话，补0
    items = data_str.split(" ")
    for i in range(len(items)):
        if len(items[i]) == 1:
            items[i] = "0" + items[i]
    # 移除所有空格
    data_str = "".join(items)
    
    # 每隔两个字符转成数字
    return bytes.fromhex(data_str)

def crc16_xmodem(data, poly=0x1021, crc=0x0000):
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if (crc & 0x8000):
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc <<= 1
    return crc

def crc16_modbus(data):
    """
    计算 Modbus CRC16 校验码
    :param data: 待计算的数据，类型为 bytes
    :return: CRC16 校验码，类型为 int
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

def add8(data, skip=0):
    """
    计算 ADD8 校验码
    """
    rst = 0x00
    for byte in data[skip:]:
        rst += byte
        
    return rst & 0xFF

def xor8(data, skip=0):
    """
    计算 XOR8 校验码
    """
    rst = 0x00
    for byte in data[skip:]:
        rst ^= byte
        
    return rst & 0xFF


def pack_protocol_data(cmd, *values):
    """按照协议打包数据
    格式如下： cmd + values
        cmd 1字节
        values 0~n个数据, 类型可以是 int, float, str
    
    :param cmd: 命令位
    :param values: 数据
    """
    data = bytes([cmd])
    for value in values:
        # 根据数据类型进行打包
        if isinstance(value, int):
            # 2字节, MSB, 高位在前
            data += struct.pack('>h', value)
        elif isinstance(value, float):
            # 4字节, MSB, 高位在前
            data += struct.pack('>f', value)
        elif isinstance(value, str):
            data += value.encode('gbk')
        elif isinstance(value, bytes):
            data += value
        else:
            raise ValueError('不支持的数据类型')
    return data

def pack_protocol_data_with_checksum(cmd, *values, header=b'\xAA\xAA', tail=b'\xBB', check_algorithm=add8):
    """按照协议打包数据，并计算校验码
    格式如下: header + cmd + len + values + checksum + tail
        header 帧头     2字节
        cmd    命令位   1字节
        len    数据长度 1字节
        values 0~n个数据, 类型可以是 int, float, str
        checksum 校验码 1字节, 内容由 check_algorithm(cmd + len + values)
        tail   帧尾     1字节
    """
    data = bytes(header)
    data += bytes([cmd])
    data_len = 0
    
    data_arr = bytes()
    # 计算数据长度 + 打包数据
    for value in values:
        if isinstance(value, int):
            data_arr += struct.pack('>h', value)
            data_len += 2
        elif isinstance(value, float):
            data_arr += struct.pack('>f', value)
            data_len += 4
        elif isinstance(value, str):
            data_arr += value.encode('gbk')
            data_len += len(value)
        elif isinstance(value, bytes):
            data_arr += value
            data_len += len(value)
        else:
            raise ValueError('不支持的数据类型')
    # 数据长度(作为一个字节)
    data += bytes([data_len])
    # 数据
    data += data_arr
    # 校验码
    checksum = check_algorithm(data, skip=2)
    data += bytes([checksum])
    # 帧尾
    data += tail
    return data


if __name__ == '__main__':
    bytes_data = b"\x01\x03\x03\x00\x00\x02"
    rst_num = crc16_modbus(bytes_data)
    
    # 输出结果是大端显示(最高位在前)
    print(hex2str(rst_num))
    
    # 将一个数字转成2个字节
    # bytes_arr = rst_num.to_bytes(2, byteorder='little')
    bytes_arr = rst_num.to_bytes(2, byteorder='big')
    # 等同于
    # little
    arr = [
        rst_num & 0xFF,
        (rst_num >> 8) & 0xFF,
    ]
    
    print(hex2str(bytes_arr))
    print(hex2str(arr))
    
    print(hex(65280))
    
    print("------------------------------")
    
    bytes_data = str2hex("01 03 02 56 31")
    crc16_rst = crc16_modbus(bytes_data)
    print(hex2str(crc16_rst))
