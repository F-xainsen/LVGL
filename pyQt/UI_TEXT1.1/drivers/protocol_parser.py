"""
协议解析器

1. 从串口读取数据
2. 将数据存到队列中
3. 根据协议解析数据

  帧头	   命令位	 数据长度	  数据位	 校验位	  帧尾
---------- ------  -------     ------     ------  -------
0xAA 0xAA	  0xB0	  0x02		待定	    待定     0xBB



"""
import sys
sys.path.append('..')
from abc import ABC, abstractmethod
import struct

from queue import Queue
from common.protocol import add8
from common.qt_worker import Worker

FRAME_HEAD = 0xAA
FRAME_TAIL = 0xBB

CMD_CURRENT    = 0xB0
CMD_PARAM_PID  = 0xB1

MAX_DATA_LEN = 33


# recv data buf
__rx_buf = []

class Response(ABC):
    
    def __init__(self):
        super().__init__()
        self.origin_array = []
        self.values = []
        
    @abstractmethod
    def set_data(self, arr) -> bytes:
        pass

    def get_values(self):
        return self.values

class PositionResponse(Response):
    def __init__(self, arr=[]):
        self.origin_array = arr
        self.set_data(arr)
        
    def set_data(self, arr) -> bytes:
        #   帧头  |   命令  |   数据长度    |   数据  |   校验码 | 帧尾
        #   2字节 |   1字节 |   1字节      |   2字节  |  1字节   | 1字节
        #    AA AA   B0         02             00 00      FF     BB    
        ###########################################################
        self.values = []
        # 将2个字节转换为int
        b = bytes()
        b += struct.pack('B', arr[4 + 0])
        b += struct.pack('B', arr[4 + 1])
        self.values.append(struct.unpack('>h', b)[0]) 

class ChannelResponse(Response):
    def __init__(self, arr=[]):
        self.origin_array = arr
        self.set_data(arr)

    def set_data(self, arr) -> bytes:
        #   帧头  |   命令  |   数据长度    |   数据  |   校验码 | 帧尾
        #   2字节 |   1字节 |   1字节      |  12字节  |  1字节   | 1字节
        #    AA AA   B1        0x0C          xxxxx       FF  BB    
        ###########################################################
        self.values = []
        c = int(arr[3] / 4)
        for i in range(c):
            # 将4个字节转换为float
            b = bytes()
            b += struct.pack('B', arr[4 + i * 4 + 0])
            b += struct.pack('B', arr[4 + i * 4 + 1])
            b += struct.pack('B', arr[4 + i * 4 + 2])
            b += struct.pack('B', arr[4 + i * 4 + 3])
            self.values.append(struct.unpack('f', b)[0])


def __make_response(arr) -> Response:
    resp: Response = None
    # 判断命令
    cmd = arr[2]
    if cmd == 0xB0:
        resp = PositionResponse(arr)
    elif cmd == 0xB1:
        resp = ChannelResponse(arr)
    return resp

def parse_response(bytes_arr):
    global __rx_buf
    if bytes_arr is not None:
        # __rx_buf.append(msg)
        __rx_buf.extend(bytes_arr)
        
    # 消息组成
    #   帧头  |   命令  |   数据长度   |   数据  |   校验码 | 帧尾
    #   2字节 |   1字节 |   1字节      |  n字节  |  1字节   | 1字节
    # 命令: 请求类型的标识
    # 数据长度: 表示后面 数据 的字节个数
    # 校验码:  命令 + 数据长度 + 数据, 取高位
    
    if len(__rx_buf) < 6:
        return None
    
    # 按照16进制打印
    # for i in __rx_buf:
    #     print(hex(i), end=' ')
    # print()
    
    # 判断是不是帧头
    if __rx_buf[0] != FRAME_HEAD:
        # 丢弃第一个
        __rx_buf.pop(0)
        return parse_response(None)
    
    if __rx_buf[1] != FRAME_HEAD:
        # 丢弃第一个
        __rx_buf.pop(0)
        return parse_response(None)
    
    # print("rx_buf: ", len(__rx_buf))
    
    cmd = __rx_buf[2]

    # 获取数据长度
    # data_len = int.from_bytes(__rx_buf[2], byteorder='big')
    data_len = __rx_buf[3]

    if data_len > MAX_DATA_LEN:
        # 丢弃第一个
        __rx_buf.pop(0)
        return parse_response(None)

    # 不够一条指令
    if len(__rx_buf) < data_len + 6:
        return None
    
    checksum = add8(__rx_buf[2:(data_len + 4)])
    # 校验验证码
    # if sum != int.from_bytes(__rx_buf[data_len + 3], byteorder='big'):
    if checksum != __rx_buf[data_len + 4]:
        # 丢弃第一个
        __rx_buf.pop(0)
        return parse_response(None)
    
    # 校验帧尾
    if __rx_buf[data_len + 5] != FRAME_TAIL:
        # 丢弃第一个
        __rx_buf.pop(0)
        return parse_response(None)
    # 全部通过
    
    total_cnt = data_len + 6
    # 取出数据
    arr = __rx_buf[:total_cnt]
    # 保留剩余数据
    __rx_buf = __rx_buf[total_cnt:]
    return __make_response(arr)

class ProtocolParser:
    
    def __init__(self, algorithm=add8):
        self.queue = Queue()
        self.data = bytes()
        self.check_algorithm = algorithm
        
        self.worker = Worker(self.long_time_handle_task)
        
    def long_time_handle_task(self, worker: Worker):
        while worker.is_running:
            # 模拟收到消息
            new_data = self.queue.get()
            # print("new_data: ", new_data)
            response = self.Get_Response(new_data)
            
            if response is not None:
               worker.emit_msg(response)

        return "refresh_worker done!"
        
    def start(self, msg_handler=None):
        self.worker.signal_connect( msg_handler = msg_handler )
        self.worker.start()
        
    def handle(self, data):
        """解析从串口读取到数据"""
        self.queue.put(data)
            
    def Get_Response(self, bytes_arr) -> Response:
        # return __parse_response(int.from_bytes(msg, byteorder='big'))
        return parse_response(bytes_arr)
