# data_provider.py
import time
import queue
from PIL import Image, ImageDraw, ImageFont
import psutil
import system_monitor as sm

# # 模拟获取 CPU 使用率数据
# def get_cpu_data():
#     return random.randint(0, 100)  # 模拟CPU使用率为0-100%

# # 模拟获取进度条相关的数据
# def get_progress_data():
#     return random.random()  # 模拟一个0-1之间的进度数据

# 模拟获取一个空白图片
def get_blank_image(width=800, height=600):
    image_path = 'D:/project/STM32F103/pyQt/UI_TEXT1.0/UI/res/3.5/swsw.png'  # 替换为你的图片路径
    image = image_path
    return image

# 模拟绘制图片上的数据
def draw_on_image(image, cpu_percent, cpu_freq, cpu_temp, 
                  memory_percent, net_up_speed, net_down_speed):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # 清除之前的绘制
    draw.rectangle([(0, 0), image.size], fill=None)

    # 绘制CPU使用率
    draw.text((10, 10), f"CPU Usage: {cpu_percent}%", font=font, fill=(0, 0, 0))
    draw.text((10, 30), f"CPU Frequency: {cpu_freq / 1000} GHz", font=font, fill=(0, 0, 0))
    draw.text((10, 50), f"CPU Temperature: {cpu_temp} °C", font=font, fill=(0, 0, 0))
    # 绘制内存使用率
    draw.text((10, 70), f"Memory Usage: {memory_percent}%", font=font, fill=(0, 0, 0))
    # 绘制网络上传下行速度
    draw.text((10, 90), f"Upload Speed: {net_up_speed / 1024:.2f} KB/s", font=font, fill=(0, 0, 0))
    draw.text((10, 110), f"Download Speed: {net_down_speed / 1024:.2f} KB/s", font=font, fill=(0, 0, 0))


    # # 绘制条形进度条
    # draw.rectangle([(50, 100), (50 + progress_data * 300, 150)], fill="blue")
    # draw.text((50, 160), f"Progress 1: {int(progress_data * 100)}%", font=font, fill=(0, 0, 0))

    # # 绘制扇形进度条
    # draw.pieslice([400, 100, 700, 400], start=0, end=progress_data2 * 360, fill="green")
    # draw.text((400, 420), f"Progress 2: {int(progress_data2 * 100)}%", font=font, fill=(0, 0, 0))

    return image

def update_image_from_queue(data_queue: queue.Queue):
    while True:
        if not data_queue.empty():
            # 从队列中获取数据
            cpu_percent, cpu_freq, cpu_temp, memory_percent, net_up_speed, net_down_speed = data_queue.get()

            # 获取空白图像
            image = get_blank_image()

            # 在图像上绘制信息
            image = draw_on_image(image, cpu_percent, cpu_freq, cpu_temp, memory_percent, net_up_speed, net_down_speed)

            # 显示图像（可以使用其他方法来显示图像，如Tkinter等）
            image.show()

            time.sleep(1)  # 控制更新频率
