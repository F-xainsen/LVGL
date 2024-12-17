import os
import numpy as np

from PIL import Image
from PyQt5.QtWidgets import QFileDialog


class Picture:
    def __init__(self):
        self.width = 320
        self.height = 240
        self.img = None
        self.path = ""
        self.size = 0
        self.data = None

    def open_img(self, window):
        res_folder = os.path.join(os.getcwd(), "resources")
        self.path, _ = QFileDialog.getOpenFileName(
            window, "打开图片", res_folder, "图片文件 (*.png;*.jpg)"
        )
        if self.path:
            self.size = os.path.getsize(self.path)
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
        # Open the image
        self.img = Image.open(self.path)
        self.img = self.img.resize((self.width, self.height))
        self.img = self.img.convert("RGB")  # Ensure the image is in RGB mode

        # Create a numpy array for RGB565 image data
        self.data = np.zeros((self.height, self.width), dtype=np.uint16)

        # Process each pixel
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.img.getpixel((x, y))
                self.data[y, x] = self.rgb_to_rgb565(r, g, b)

    def rgb565_to_rgb(self, rgbs565):
        """Convert RGB565 back to 8-bit RGB."""
        r = (rgbs565 >> 11) & 0x1F
        g = (rgbs565 >> 5) & 0x3F
        b = rgbs565 & 0x1F
        return (r << 3, g << 2, b << 3)

    def display_rgb565_image(self):
        """Convert RGB565 image back to RGB for display."""
        height, width = self.data.shape
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                rgb_image[y, x] = self.rgb565_to_rgb(self.data[y, x])

        img = Image.fromarray(rgb_image)
        img.show()
