import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import random
import time
import math
import numpy as np
# from watermark import Watermark

class ProgressBar:
    def __init__(self, image_path, font_path='arial.ttf', font_size=10):
        # 加载背景图片
        self.img = Image.open(image_path).convert("RGB")
        self.width, self.height = self.img.size
        self.font = ImageFont.truetype(font_path, font_size)  # 设置字体
        self.position = (10, 10)  # 文字的起始位置
        self.bar_height = 10  # 进度条的高度
        self.max_width = 80  # 进度条最大宽度
        # self.queue = queue  # 用于接收数据的队列

        # 扇形进度条的配置
        self.radius = min(self.width, self.height) // 8  # 扇形进度条半径
        self.center = (self.width // 6, self.height // 3)  # 扇形中心点
        
        # # 初始化 Watermark 类
        # self.watermark = Watermark(image_path, font_path, font_size)
        # 水印位置
        # self.watermark_position = (240, 10)
        # self.original_img = self.img.copy()  # 保持一份原始图片

    def draw_bar(self, draw, progress):
        # 绘制条形进度条
        bar_width = int(self.max_width * progress)  # 进度条的宽度
        draw.rectangle([10, 24, 10 + bar_width, 30], fill="blue")  # 进度条本体

        # 绘制进度百分比文本
        text = f"CPU Usage: {int(progress * 100)}%"
        draw.text(self.position, text, font=self.font, fill="black")

    def draw_circle(self, draw, progress):
        # 计算进度条的角度
        angle = 360 * progress  # 进度条弧度

        # 绘制扇形进度条
        draw.arc(
            [self.center[0] - self.radius, self.center[1] - self.radius,
             self.center[0] + self.radius, self.center[1] + self.radius],
            start=90, end=90 + angle, fill="red", width=10)  # 绘制进度弧线

        # 绘制温度文本
        text = f"{int(progress * 100)}°C"
        text_bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = (self.center[0] - text_width // 2, self.center[1] - text_height // 2)
        draw.text(text_position, text, font=self.font, fill="black")

    def update_image(self, cpu_progress, temp_progress):
        # 复制原始图片以避免修改原图
        img_copy = self.img.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # 获取当前时间并作为水印
        # img_copy = self.watermark.update_image(img_copy)

        # 绘制条形进度条
        self.draw_bar(draw, cpu_progress)

        # 绘制扇形进度条
        self.draw_circle(draw, temp_progress)
        
        # self.ax.imshow(img_copy)
        # plt.draw()
        # img_copy = np.array(img_copy)
        
        return img_copy

    def show_image(self, img_copy):
        # 使用matplotlib显示更新后的图像
        plt.imshow(img_copy)
        plt.axis('off')  # 不显示坐标轴
        plt.draw()  # 刷新图像
        plt.pause(1)  # 每0.1秒刷新一次图像
        
    
    
    def run(self):
        plt.ion()  # 开启交互模式
        plt.figure(figsize=(6, 6))  # 设置图像显示大小

        while True:
            # 随机生成进度条的进度（范围0到1），模拟CPU占用率和温度
            cpu_progress = random.random()  # 随机生成一个0到1之间的浮动值，模拟CPU占用率
            temp_progress = random.random()  # 随机生成一个0到1之间的浮动值，模拟CPU温度

            # 更新图像
            img_copy = self.update_image(cpu_progress, temp_progress)
            self.show_image(img_copy)

            # 等待一段时间后再次更新进度条
            # time.sleep(1)  # 每秒更新一次

        plt.ioff()  # 关闭交互模式
        plt.show()  # 显示最终图像
        
        
    # def run(self):
    #     while True:
    #         if not self.queue.empty():
    #             cpu_progress = self.queue.get()  # 从队列中获取 CPU 进度值
    #             img_copy = self.update_bar(cpu_progress)
    #             self.animate(cpu_progress, img_copy)
    #         time.sleep(1)
   


# 示例用法：
image_path = 'D:/project/STM32F103/pyQt/UI_TEXT1.0/UI/res/3.5/swsw.png'  # 这里替换成你的图片路径
progress_bar = ProgressBar(image_path)
progress_bar.run()

# def progress_bar_thread(queue):
#     """ 用于更新进度条的线程 """
#     while True:
#         # 模拟 CPU 占用率的进度条（随机）
#         cpu_progress = random.random()
#         queue.put(cpu_progress)  # 将进度条的值传递给队列
#         # time.sleep(1)

# def main():
#     # 创建一个队列，用于线程之间通信
#     queue = Queue()

#     # 创建进度条对象
#     progress_bar = ProgressBar(image_path="D:/project/STM32F103/pyQt/UI_TEXT1.0/UI/res/3.5/swsw.png", queue=queue)

#     # 启动动态时间更新的线程
#     time_thread_instance = threading.Thread(target=time_thread, args=(queue,))
#     time_thread_instance.daemon = True  # 设置为守护线程
#     time_thread_instance.start()

#     # 启动进度条更新的线程
#     progress_thread_instance = threading.Thread(target=progress_bar_thread, args=(queue,))
#     progress_thread_instance.daemon = True  # 设置为守护线程
#     progress_thread_instance.start()

#     # 使用 FuncAnimation 动态更新图像
#     plt.ion()
#     plt.show()

#     # 运行主循环
#     progress_bar.run()


# if __name__ == "__main__":
#     main()