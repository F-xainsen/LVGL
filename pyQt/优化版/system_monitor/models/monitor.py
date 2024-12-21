import psutil
import win32com.client

# from pycaw.pycaw import AudioUtilities
# from pycaw.pycaw import IAudioEndpointVolume

import queue
import time 

class SystemMonitor:

    def __init__(self):
        # self.data_queue = data_queue or queue.Queue
        self.cpu_percent = 0
        self.cpu_freq = 0
        self.cpu_temperature = 0
        self.memory: psutil.svmem = None
        self.net = None
        self.net_before = None
        self.net_up_speed = 0
        self.net_down_speed = 0
        self.volume = 0.0

    def update_all(self):
        self.cpu_percent, self.cpu_freq, self.cpu_temperature = SystemMonitor.get_cpu_info()
        self.memory = SystemMonitor.get_memory_info()

        self.net_before = self.net
        self.net = SystemMonitor.get_net_info()

        if self.net_before != None:
            self.net_up_speed = self.net.bytes_sent - self.net_before.bytes_sent
            self.net_down_speed = self.net.bytes_recv - self.net_before.bytes_recv

        #self.volume = SystemMonitor.get_volume_precent()
        # 将更新后的数据传递给队列
        # self.data_queue.put((self.cpu_percent, 
        #                      self.cpu_freq, 
        #                      self.cpu_temperature, 
        #                      self.memory.percent, 
        #                      self.net_up_speed, 
        #                      self.net_down_speed))


    def __str__(self):
        return (f"System Monitor:\n"
                f"CPU占用率: {self.cpu_percent}%\n"
                f"CPU主频: {self.cpu_freq / 1000} GHz\n"
                f"CPU温度: {self.cpu_temperature} °C\n"
                # f"GPU: {self.gpu_name}\n"
                # f"GPU温度: {self.gpu_temp} °C\n"
                # f"GPU占用率: {self.gpu_usage}%\n"
                f"内存占用率: {self.memory.percent}%\n"
                f"上传速度: {self.net_up_speed / 1024:.2f} KB/s\n"
                f"下传速度: {self.net_down_speed / 1024:.2f} KB/s")

    @staticmethod
    def get_cpu_info():
        percent = psutil.cpu_percent()
        freq = psutil.cpu_freq().current
        temperature = SystemMonitor.get_cpu_temperature()
        return percent, freq, temperature

    @staticmethod
    def get_cpu_temperature() -> float:
        try:
            # 连接到 WMI
            wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            conn = wmi.ConnectServer(".", "root\\wmi")

            # 查询温度传感器数据
            sensors = conn.ExecQuery(
                "SELECT * FROM MSAcpi_ThermalZoneTemperature")
            temp = sensors[0].CurrentTemperature
            celsius = (temp - 2732) / 10.0
            return celsius
            # for sensor in sensors:
            #     # 获取当前温度，单位为千开尔文 (mK)，转换为摄氏度
            #     temp = sensor.CurrentTemperature
            #     celsius = (temp - 2732) / 10.0  # 转换为摄氏度
            #     print(f"Temperature: {celsius:.1f}°C")
        except:
            return 0.0

    @staticmethod
    def get_memory_info():
        return psutil.virtual_memory()

    @staticmethod
    def get_net_info():
        return psutil.net_io_counters()

    # @staticmethod
    # def get_volume_precent():
    #     # 获取默认音频设备
    #     devices = AudioUtilities.GetSpeakers()
    #     interface = devices.Activate(
    #         IAudioEndpointVolume._iid_, 1, None)

    #     # 获取音量
    #     volume = interface.QueryInterface(IAudioEndpointVolume)
    #     volume = volume.GetMasterVolumeLevelScalar()  # 返回范围 0.0 到 1.0
    #     return volume * 100  # 转换为百分比

    @staticmethod
    def get_gpu_info_wmi():
        try:
            wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            conn = wmi.ConnectServer(".", "root\\cimv2")
            query = "SELECT * FROM Win32_VideoController"
            video_controllers = conn.ExecQuery(query)

            for controller in video_controllers:
                # print(f"显卡名称: {controller.Name}")
                # print(f"显存: {controller.AdapterRAM / (1024 ** 2):.2f} MB")
                # print(f"驱动程序: {controller.DriverVersion}")
                if "Intel" in controller.Name:
                    pass
                elif "NVIDIA" in controller.Name:
                    pass
                elif "AMD" in controller.Name:
                    pass

        except:
            pass

    # def run(self):
    #     """定时更新系统信息"""
    #     # print(time)
    #     while True:
    #         self.update_all()
    #         # time.sleep(1)  # 每秒更新一次