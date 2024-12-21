import unittest
import logging
import time

from models.device import Device
from models.picture import Picture

class TestSerial(unittest.TestCase):
    def test_picture_send():
        device = Device()
        ports = device.scan()