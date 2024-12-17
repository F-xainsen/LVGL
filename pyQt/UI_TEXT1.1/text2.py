import psutil
import cpuinfo
import subprocess
import wmi

def get_cpu_info():
    # 获取CPU信息
    cpu_info = cpuinfo.get_cpu_info()
    
    # 获取 CPU 实际主频，可能是列表类型
    cpu_frequency = cpu_info.get('hz_actual', ['未知'])[0]  # 如果是列表，取第一个元素
    
    # 获取 CPU 占用率
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # 获取 CPU 温度（仅在支持的系统上可用）
    # cpu_temp = None
    # temps = psutil.sensors_temperatures()
    # if "coretemp" in temps:
    #     cpu_temp = temps["coretemp"][0].current
    
    return cpu_usage, cpu_frequency

# def get_cpu_temp():
#     w = wmi.WMI(namespace="root\\wmi")
#     temperature_info = w.MSAcpi_ThermalZoneTemperature()
    
#     if temperature_info:
#         # 获取温度数据（单位为十进制温度乘以10，需要除以10来转换）
#         temp = temperature_info[0].CurrentTemperature / 10.0 - 273.15  # 转换为摄氏度
#         return temp
#     return None

# cpu_temp = get_cpu_temp()

def get_gpu_info():
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

def get_memory_info():
    # 获取内存占用率
    memory = psutil.virtual_memory()
    memory_usage = memory.percent  # 内存使用百分比
    return memory_usage

def get_network_speed():
    # 获取网络接口的上传和下载速度
    net_io = psutil.net_io_counters(pernic=False)  # 获取总网卡流量
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv

    # 将流量从字节转换为MB
    upload_speed = bytes_sent / 1024 / 1024  # 转换为MB
    download_speed = bytes_recv / 1024 / 1024  # 转换为MB

    return upload_speed, download_speed

# 获取CPU信息
cpu_usage, cpu_frequency = get_cpu_info()
if isinstance(cpu_frequency, int):
    cpu_frequency_ghz = cpu_frequency / 1_000_000_000  # 转换为GHz
    print(f"CPU占用率: {cpu_usage}%")
    print(f"CPU主频: {cpu_frequency_ghz:.2f} GHz")
else:
    print(f"无法获取有效的CPU主频")
    
# if cpu_temp:
#     print(f"CPU温度: {cpu_temp}°C")
# else:
#     print("无法获取CPU温度")

# 获取GPU信息
gpu_name, gpu_temp, gpu_usage = get_gpu_info()
if gpu_name:
    print(f"显卡名称: {gpu_name}")
    print(f"显卡温度: {gpu_temp}°C")
    print(f"显卡占用率: {gpu_usage}%")
else:
    print("无法获取显卡信息")

# 获取内存信息
memory_usage = get_memory_info()
print(f"内存占用率: {memory_usage}%")

# 获取网络速度
upload_speed, download_speed = get_network_speed()
print(f"上传速度: {upload_speed:.2f} MB/s")
print(f"下载速度: {download_speed:.2f} MB/s")
