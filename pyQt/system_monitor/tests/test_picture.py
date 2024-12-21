import unittest
import logging
import time
from models.picture import Picture

from PIL import Image, ImageDraw, ImageFont


class PictureMonitor(unittest.TestCase):
    def test_drawText(self):
        p = Picture()
        p.path = "resources\\a.png"
        p.img = Image.open(p.path)
        p.img = p.img.convert("RGB")
        p.data = p.draw_text_img("Line1\nLine2",(10,10))
        # p.display_rgb565_image()
        p.draw_sidebar_img((30,50),100,10,20)