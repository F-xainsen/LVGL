import unittest
import logging
import time
from models.monitor import SystemMonitor


class TestSystemMonitor(unittest.TestCase):
    def test_get_cpu_info(self):
        SystemMonitor.get_cpu_info()  # ignore first time value
        time.sleep(1)  # wait to update
        precent, freq, _ = SystemMonitor.get_cpu_info()
        logging.info([precent, freq])
        self.assertIsInstance(precent, float)
        self.assertGreaterEqual(precent, 0)
        self.assertLessEqual(precent, 100)
        self.assertNotEqual(precent, 0)

        self.assertIsInstance(freq, float)
        self.assertGreaterEqual(freq, 0)
        self.assertNotEqual(freq, 0)

    def test_get_memory_info(self):
        memory_info = SystemMonitor.get_memory_info()

        self.assertGreater(memory_info.total, 0)
        self.assertGreaterEqual(memory_info.percent, 0)
        self.assertLessEqual(memory_info.percent, 100)
        logging.info(memory_info)

    def test_get_net_info(self):
        net_before = SystemMonitor.get_net_info()
        time.sleep(1)
        net_after = SystemMonitor.get_net_info()

        up_speed = net_after.bytes_sent - net_before.bytes_sent
        down_speed = net_after.bytes_recv - net_before.bytes_recv

        logging.info(
            f"上传速度: {up_speed / 1024:.2f} KB/s | 下载速度: {down_speed / 1024:.2f} KB/s")

    def test_get_volume(self):
        volume = SystemMonitor.get_volume_precent()
        self.assertGreaterEqual(volume, 0)
        self.assertLessEqual(volume, 100)
        logging.info(volume)

if __name__ == '__main__':
    unittest.main()
