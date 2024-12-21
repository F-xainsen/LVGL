import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from models.device import Device
from models.monitor import SystemMonitor
from models.picture import Picture


class serialController:
    def __init__(self, device: Device, data):
        self.device = device
        self.data = data

    def send(self):
        self.thread = SerialThread(self.device, self.data)
        self.thread.start()


class SerialThread(QThread):
    def __init__(self, device: Device, data):
        super().__init__()
        self.device = device
        self.data = data

    def run(self):
        if self.device and self.device.get_state():
            self.device.device.write(self.data)
