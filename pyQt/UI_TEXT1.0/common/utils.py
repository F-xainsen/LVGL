import os
import struct
import time
import socket
import ipaddress

def get_local_ip():
    """
    获取本机所有IP
    :return: IP列表
    """
    local_ips = ["127.0.0.1"]
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        local_ips.append(ip)

    local_ips.sort(reverse=True)
    return local_ips

class Color:
    """
    颜色枚举类
    """
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36


def wrap_color(msg, color):
    """
    包装颜色
    :param msg: 要包装的字符串
    :param color: 颜色
    :return:
    """
    return f"\033[{color}m{msg}\033[0m"


def calculate_broadcast_address(host, mask_bits):
    # 将主机IP地址和掩码位数转换为网络对象
    network = ipaddress.ip_network(f"{host}/{mask_bits}", strict=False)

    # 获取广播地址
    broadcast_address = network.broadcast_address

    # 返回广播地址的字符串表示形式
    return str(broadcast_address)


def current_time_str():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def decode_data(recv_data: bytes):
    try:
        recv_msg = recv_data.decode("utf-8")
    except:
        try:
            recv_msg = recv_data.decode("gbk")
        except:
            recv_msg = recv_data
            
    return recv_msg

def clear_console():
    # 使用ANSI转义序列清空控制台内容
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    print(get_local_ip())
