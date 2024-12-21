import os
import time
from models.monitor import SystemMonitor
from views.Ui_main_window import Ui_MainWindow
from models.device import Device
from models.picture import Picture
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from controller.serialController import serialController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.device = Device()
        self.img = Picture()
        self.monitor = SystemMonitor()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_monitor)
        self.timer.start(1000)

        self.controller = serialController(self.device,None)

    def init_ui(self):
        self.ui.update_button.clicked.connect(self.update_serial_port)
        self.ui.open_image.clicked.connect(self.update_image)

        self.ui.run_button.clicked.connect(self.on_run)
        self.ui.stop_button.clicked.connect(self.on_stop)

    @pyqtSlot()
    def update_serial_port(self):
        ports = self.device.scan()
        self.ui.serial_port_combobox.clear()
        ports = [port.device for port in ports]
        self.ui.serial_port_combobox.addItems(ports)

        if (len(ports)):  # set first to default
            self.device.port = ports[0]

    @pyqtSlot()
    def update_image(self):
        self.img.open_img(self)
        if self.img.path:
            # 显示选择的文件名
            self.ui.fileEdit.setText(self.img.path)
            # 显示图片大小
            self.ui.sizeEdit.setText(f"{self.img.size} bytes")
            try:
                pixmap = QImage(self.img.path)
                if pixmap.isNull():
                    # 如果加载的图片为空，显示错误消息
                    QMessageBox.warning(self, "打开失败", "无法加载此图片，请检查文件格式")
                    return
                pixmap = pixmap.scaled(
                    self.img.width, self.img.height, aspectRatioMode=Qt.KeepAspectRatio)
                self.ui.view.setPixmap(QPixmap.fromImage(pixmap))
                self.ui.view.setScaledContents(True)
                self.img.convert_image_to_rgb565()
                
            except Exception as e:
                QMessageBox.warning(self, "打开失败", f"发生错误：{str(e)}")

    @pyqtSlot()
    def on_run(self):
        if not self.device.device or not self.device.device.is_open:
            self.img.open_with_path()
            self.img.draw_text_img(str(self.monitor),(10,10))

            self.img.draw_sidebar_img((30,200),(100 * (self.monitor.cpu_percent / 100)),10,10)
            self.img.convert_image_to_rgb565()
            self.controller.data = self.img.oridata
            self.device.connect()
            self.controller.send()
            self.img.img.show()

    @pyqtSlot()
    def on_stop(self):
        if self.device.device and self.device.device.is_open:
            self.device.device.close()
        pass

    @pyqtSlot()
    def display_monitor(self):
        self.monitor.update_all()
        self.ui.info_label.setText(str(self.monitor))
