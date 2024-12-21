import serial
import serial.tools.list_ports


class Device:
    def __init__(self):
        self.device: serial.Serial = None
        self.baudrate = 115200
        self.port = ""
        self.bytesize = 8
        self.parity = 'N'
        self.stopbits = 1
        self.xonxoff = False
        self.rtscts = False
        self.dsrdtr = False
        self.timeout = None
        self.write_timeout = None

    def get_state(self) -> bool:
        if self.device:
            return self.device.is_open
        return False

    def connect(self):
        if self.port != "":
            self.device = serial.Serial(
                baudrate=self.baudrate,
                port=self.port,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                xonxoff=self.xonxoff,
                rtscts=self.rtscts,
                dsrdtr=self.dsrdtr,
                timeout=self.timeout,
                write_timeout=self.write_timeout
            )

    def scan(self):
        return serial.tools.list_ports.comports()
