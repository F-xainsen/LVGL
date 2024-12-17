from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QFont
from PyQt5.QtCore import Qt

class ImageWithTextWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('图片上叠加硬件信息')

        # 初始化 UI 界面
        self.init_ui()

        # 获取硬件信息
        self.cpu_usage = 45.5  # 假设 CPU 使用率为 45.5%
        self.gpu_temp = 60.0  # 假设 GPU 温度为 60°C
        self.memory_usage = 70.3  # 假设内存使用率为 70.3%

        # 加载图片并在其上绘制硬件信息
        self.load_and_display_image()

    def init_ui(self):
        """初始化用户界面"""
        # 创建显示图片的标签
        self.label = QLabel(self)
        self.setCentralWidget(self.label)

    def load_and_display_image(self):
        """加载图片并在其上叠加硬件信息"""
        # 加载图片（假设图片路径为 'image.png'）
        pixmap = QPixmap('UI/res/3.5/back0.png')  # 相对路径


        # 检查图片是否加载成功
        if pixmap.isNull():
            print("图片加载失败")
            return

        # 将 QPixmap 转换为 QImage 以便于绘制文本
        image = pixmap.toImage()

        # 创建 QPainter 对象，用于绘制文本
        painter = QPainter(image)

        # 设置字体和颜色
        painter.setFont(QFont("Arial", 12))
        painter.setPen(Qt.white)  # 设置文本颜色为白色

        # 在图片上绘制文本（CPU、GPU 和内存信息）
        painter.drawText(10, 30, f"CPU 使用率: {self.cpu_usage}%")
        painter.drawText(10, 60, f"GPU 温度: {self.gpu_temp}°C")
        painter.drawText(10, 90, f"内存使用率: {self.memory_usage}%")

        # 结束绘制
        painter.end()

        # 将处理过的 QImage 转换回 QPixmap 并显示在标签上
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setAlignment(Qt.AlignCenter)  # 图片居中显示
        # 调整图片适应标签大小
        self.label.setScaledContents(True)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ImageWithTextWindow()
    window.show()
    sys.exit(app.exec_())
