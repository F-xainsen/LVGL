import psutil
import cpuinfo
import subprocess
from PyQt5.QtCore import *
import wmi



class GetCPUInfo(QThread):
    # 定义信号，用来传递CPU、GPU、内存、网络信息
    cpu_info_signal = pyqtSignal(list)
    gpu_info_signal = pyqtSignal(list)
    memory_info_signal = pyqtSignal(list)
    network_info_signal = pyqtSignal(list)
    stop_signal = pyqtSignal()  # 用于停止线程
    
    
        
    def __init__(self):
        super().__init__()
        self.running = True  # 标志是否继续运行
        self.stopped = False  # 标志是否停止

        
    def run(self):
        while self.running:
            
            # 获取CPU信息
            cpu_usage, cpu_frequency, cpu_temperature= self.get_cpu_info()
            self.cpu_info_signal.emit([cpu_usage, cpu_frequency, cpu_temperature])
            # cpu_info = f"CPU占用率: {cpu_usage}%\nCPU主频: {cpu_frequency} GHz\nCPU温度: {cpu_temperature}°C"            
            #self.cpu_info_signal.emit(cpu_info)
            # print(cpu_info)

            # 获取GPU信息
            gpu_name, gpu_temp, gpu_usage = self.get_gpu_info()
            self.gpu_info_signal.emit([gpu_name, gpu_temp, gpu_usage])
            # gpu_info = f"显卡名称: {gpu_name}\n温度: {gpu_temp}°C\n占用率: {gpu_usage}%"       
            # print(gpu_info)

            # 获取内存信息
            memory_usage = self.get_memory_info()
            self.memory_info_signal.emit([memory_usage])
            # memory_info = f"内存占用率: {memory_usage}%"
            # print(memory_info)

            # 获取网络速度
            upload_speed, download_speed = self.get_network_speed()
            self.network_info_signal.emit([upload_speed, download_speed])
            # network_info = f"上传速度: {upload_speed:.2f} MB/s\n下载速度: {download_speed:.2f} MB/s"              
            # print(network_info)
            
        # print("子线程退出")  # 线程退出时输出
        
    def stop(self):
        """停止线程"""
        if  self.running:
            self.stopped = True  # 标记为已停止
            self.running = False
            self.stop_signal.emit()  # 发出停止信号
            self.quit()  # 停止线程的事件循环
            # self.wait()  # 等待线程完全退出
            
        
    def get_cpu_info(self):
        # 获取CPU信息
        cpu_info = cpuinfo.get_cpu_info()
        # 获取 CPU 实际主频，可能是列表类型
        cpu_frequency = cpu_info.get('hz_actual', ['未知'])[0]  # 如果是列表，取第一个元素
        # 获取 CPU 占用率
        cpu_usage = psutil.cpu_percent(interval=1)
        #获取CPU温度
        cpu_temperature = self.get_cpu_temperature()
        
        return cpu_usage, cpu_frequency / 1_000_000_000 ,cpu_temperature # 转换为GHz
    
    def get_cpu_temperature(self):
        return 0.0  # 待实现
        # 获取 CPU 温度（Windows 系统）
        try:
            temperatures = psutil.sensors_temperatures()
            if 'coretemp' in temperatures:
                # 返回第一个核心的温度，或根据系统选择合适的传感器
                return temperatures['coretemp'][0].current
        except Exception as e:
            print(f"获取CPU温度失败: {e}")
            return None

    def get_gpu_info(self):
        # 使用nvidia-smi获取显卡信息（仅限NVIDIA显卡）
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=gpu_name,temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                gpu_info = result.stdout.strip().split('\n')[0].split(', ')
                gpu_name = gpu_info[0]
                gpu_temp = gpu_info[1]
                gpu_usage = gpu_info[2]
                return gpu_name, gpu_temp, gpu_usage
            else:
                return None, None, None
        except Exception as e:
            print(f"显卡信息获取失败: {e}")
            return None, None, None

    def get_memory_info(self):
        # 获取内存占用率
        memory = psutil.virtual_memory()
        memory_usage = memory.percent  # 内存使用百分比
        return memory_usage

    def get_network_speed(self):
        # 获取网络接口的上传和下载速度
        net_io = psutil.net_io_counters(pernic=False)  # 获取总网卡流量
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv

        # 将流量从字节转换为MB
        upload_speed = bytes_sent / 1024 / 1024  # 转换为MB
        download_speed = bytes_recv / 1024 / 1024  # 转换为MB
        # 保留两位小数
        upload_speed = round(upload_speed, 2)
        download_speed = round(download_speed, 2)
        
        return upload_speed, download_speed
    
if __name__ == '__main__':
    
    upload_speed, download_speed = GetCPUInfo().get_network_speed() 
    print("upload_speed:", upload_speed, "MB/s")
    print("download_speed:", download_speed, "MB/s")