import matplotlib.pyplot as plt    
from PIL import Image, ImageDraw, ImageFont
import time
import datetime

class Watermark:
    def __init__(self, image_path, font_path='arial.ttf', font_size=20):
        # 加载图片
        self.img = Image.open(image_path)  # 图片路径
        self.font = ImageFont.truetype(font_path, font_size)  # 设置字体
        self.position = (240, 10)  # 水印位置，左上角，你可以根据需要调整
        self.original_img = self.img.copy()  # 保持一份原始图片
    
    def get_current_time(self):
        # 获取当前时间
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")  # 格式化为 24 小时制时间

    def update_image(self, number=None):
        # 复制原始图片以避免修改原图
        img_copy = self.original_img.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # 获取当前时间
        if number is None:
            number = self.get_current_time()

        # 清除旧的数字（水印） - 这里只是做一个简单的矩形清除，如果有复杂背景需要更复杂的处理
        draw.rectangle([self.position, (self.position[0] + 78, self.position[1] + 20)], fill=None)  # 清除旧水印区域

        # 绘制新的数字（时间）
        draw.text(self.position, str(number), font=self.font, fill="red")
        
        # 返回更新后的图片
        return img_copy
    
    
# def time_thread(queue):
# # """ 用于更新动态时间的线程 """
#     while True:
#         current_time = datetime.datetime.now().strftime("%H:%M:%S")
#         # 将时间传递给队列
#         queue.put(current_time)
#         time.sleep(1)
    
    def show_image(self, img_copy):
        # 显示更新后的图像
        plt.imshow(img_copy)
        plt.axis('off')  # 不显示坐标轴
        plt.draw()  # 刷新图像
        plt.pause(1)  # 每1秒刷新一次图像
        
    def run(self):
        # 启动实时更新时间
        plt.ion()  # 开启交互模式
        plt.figure(figsize=(6, 6))  # 设置图像显示大小

        while True:
            # 更新图像并显示
            img_copy = self.update_image()
            self.show_image(img_copy)
            

watermark = Watermark('D:/project/STM32F103/pyQt/UI_TEXT1.0/UI/res/3.5/swsw.png')
watermark.run()

