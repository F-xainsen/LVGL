import serial
from serial import Serial
from serial.tools import list_ports


def scan_serial_ports():
    ports = list_ports.comports()
    # for port in serial_ports: # ListPortInfo
    #     print(port.device, port.description, port.hwid, port.vid, port.pid, port.serial_number, port.location)
    return [(port.device, port.description) for port in ports]


class SerialDevice:
    def __init__(self, port, baudrate=115200, timeout=None, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.kwargs = kwargs
        self.serial: Serial = None
        

    def open(self):
        try:
            self.serial = serial.Serial(
                self.port, self.baudrate, timeout=self.timeout,
                **self.kwargs
            )
            self.serial.set_buffer_size(rx_size=4096)
            if self.serial.is_open:
                # print(f"Serial port {self.port} opened successfully.")
                return True, f"Serial port {self.port} opened successfully."
        except serial.SerialException as e:
            print("请检查设备是否连接，或端口被其他软件占用，Failed to open serial port:", str(e))
            return False, str(e)

        return False, f"Serial port {self.port} open failed."

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Serial port closed.")
        else:
            print("Serial port is not open.")

    def write(self, data):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None

        try:
            self.serial.write(data)
            print("Data written:", data)
        except serial.SerialException as e:
            print("Failed to write data:", str(e))

    def flush(self):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None

        self.serial.flush()

    def read(self, num_bytes = 1):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return None
        try:
            return self.serial.read(num_bytes)
        except serial.SerialException as e:
            print("Failed to read data:", str(e))
        except Exception as e:
            print("Read data err:", str(e))

        return None

    def readline(self):
        if not self.serial or not self.serial.is_open:
            print("Serial port is not open.")
            return

        try:
            # self.serial.in_waiting()
            
            return self.serial.readline()
        except serial.SerialException as e:
            print("Failed to read data:", str(e))
        except Exception as e:
            print("Read data err:", str(e))

        return None

    def is_open(self):
        if not self.serial:
            return False

        return self.serial.is_open


if __name__ == '__main__':

    # 示例用法
    serial_ports = scan_serial_ports()
    if len(serial_ports) > 0:
        print("Available serial serial_ports:")
        for device, description in serial_ports:
            print(device, "---", description)
    else:
        print("No serial serial_ports found.")

    # 示例用法
    # sp = SerialDevice("COM1", baud_rate=9600, timeout=1)  # 替换为您的串口名称、波特率和超时时间
    # sp.open()
    # sp.write(b"Hello, Serial!")  # 发送数据
    # sp.read(10)  # 读取10个字节的数据
    # sp.close()
