import os
import numpy as np

from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QFileDialog


class Picture:
    def __init__(self):
        self.width = 320
        self.height = 240
        self.img = None
        self.path = ""
        self.size = 0
        self.data = None
        self.oridata = self.data

    def open_img(self, window):
        res_folder = os.path.join(os.getcwd(), "resources")
        self.path, _ = QFileDialog.getOpenFileName(
            window, "打开图片", res_folder, "图片文件 (*.png;*.jpg)"
        )
        if self.path:
            self.size = os.path.getsize(self.path)
            # Open the image
            self.img = Image.open(self.path)
            self.img = self.img.resize((self.width, self.height))
            self.img = self.img.convert("RGB")  # Ensure the image is in RGB mode
        else:
            self.size = 0

    def open_with_path(self):
        if self.path:
            self.size = os.path.getsize(self.path)
            # Open the image
            self.img = Image.open(self.path)
            self.img = self.img.resize((self.width, self.height))
            self.img = self.img.convert("RGB")  # Ensure the image is in RGB mode
        else:
            self.size = 0

    def rgb_to_rgb565(self, r, g, b):
        """Convert a single pixel from RGB to RGB565."""
        r_5bits = (r >> 3) & 0x1F
        g_6bits = (g >> 2) & 0x3F
        b_5bits = (b >> 3) & 0x1F
        return (r_5bits << 11) | (g_6bits << 5) | b_5bits

    def convert_image_to_rgb565(self):
        """Convert an image to RGB565 format."""
        # Create a numpy array for RGB565 image data
        self.data = np.zeros((self.height, self.width), dtype=np.uint16)

        # Process each pixel
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.img.getpixel((x, y))
                self.data[y, x] = self.rgb_to_rgb565(r, g, b)

        self.oridata = self.data

    def rgb565_to_rgb(self, rgbs565):
        r = ((rgbs565 >> 11) & 0x1F) << 3
        g = ((rgbs565 >> 5) & 0x3F) << 2
        b = (rgbs565 & 0x1F) << 3
        return np.dstack((r, g, b))
        """Convert RGB565 back to 8-bit RGB."""
        r = (rgbs565 >> 11) & 0x1F
        g = (rgbs565 >> 5) & 0x3F
        b = rgbs565 & 0x1F
        return (r << 3, g << 2, b << 3)

    def display_rgb565_image(self):
        """Convert RGB565 image back to RGB for display."""
        rgb_image = np.zeros((self.height,self.width, 3), dtype=np.uint8)

        for y in range(self.height):
            for x in range(self.width):
                rgb_image[y, x] = self.rgb565_to_rgb(self.data[y, x])

        img = Image.fromarray(rgb_image)
        img.show()

    # 绘制文字空白画布
    def draw_text_canvas(self,text, position, font_file="arial.ttf"):
        # 创建带透明背景的空白图像
        canvas = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype(font_file, 10)
        draw.text(position, text, fill=(255, 255, 255), font=font)

        data = np.zeros((self.height, self.width), dtype=np.uint16)
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = canvas.getpixel((x, y))
                data[y, x] = self.rgb_to_rgb565(r, g, b)
        return data
    
    # 绘制文字
    def draw_text_img(self,text, position, font_file="Deng.ttf"):
        if self.img:
            draw = ImageDraw.Draw(self.img)
            font = ImageFont.truetype(font_file, 10)
            draw.text(position, text, fill=(255, 255, 255), font=font)
    
            data = np.zeros((self.height, self.width), dtype=np.uint16)
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = self.img.getpixel((x, y))
                    data[y, x] = self.rgb_to_rgb565(r, g, b)
            return data
        return None
    
    def draw_sidebar_img(self,position,width,height,radius=0):
        if self.img:
            draw = ImageDraw.Draw(self.img)
            x,y = position
            draw.rounded_rectangle([x, y, x+width, y+height], fill=(255, 255, 255),radius=radius)
    
    # # 更新RGB565图片中的文字
    # def apply_text_to_rgb565(self, text_image):
    #     # 检测透明像素 (0, 0, 0, 0)
    #     mask = text_image[..., 3] > 0  # 检查Alpha通道是否大于0
    #     rgb_text = text_image[..., :3]

    #     # 提取现有RGB565数据为RGB格式，确保返回可变的NumPy数组
    #     current_rgb = np.array(self.rgb565_to_rgb(self.data), dtype=np.uint8)  # 转为可变数组

    #     # 获取非透明像素的位置
    #     y_indices, x_indices = np.where(mask)

    #     # 更新现有RGB图像
    #     current_rgb[y_indices, x_indices] = rgb_text[y_indices, x_indices]

    #     # 转回RGB565格式
    #     self.data = self.rgb_to_rgb565(current_rgb)