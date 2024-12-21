import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class ProgressBar(QWidget):
    def __init__(self, image_path, font_size=10):
        super().__init__()
        self.setWindowTitle("Dynamic Progress Bar")
        self.setGeometry(100, 100, 400, 400)

        self.image_path = image_path
        self.font = QFont('Arial', font_size)
        self.max_width = 200
        self.bar_height = 10

        self.cpu_percent = 0.0
        self.cpu_freq = 0.0
        self.cpu_temperature = 0.0
        self.memory = 0.0
        self.net_up_speed = 0.0
        self.net_down_speed = 0.0

        self.image = QImage(self.image_path)
        self.pixmap = QPixmap(self.image)

        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())

        # Start a timer to update the progress
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)  # Update every second

    def draw_bar(self, painter, y_position, progress, label):
        bar_width = float(self.max_width * progress)
        painter.setBrush(QColor(0, 0, 255))  # Blue color for bar
        painter.drawRect(10, y_position, bar_width, self.bar_height)

        painter.setPen(QColor(0, 0, 0))  # Black color for text
        painter.setFont(self.font)
        text = f"{label}: {float(progress * 100)}%"
        painter.drawText(10, y_position - 10, text)

    def draw_circle(self, painter, progress, y_position, label):
        radius = min(self.pixmap.width(), self.pixmap.height()) // 8
        center = (self.pixmap.width() // 2, y_position)
        angle = 360 * progress

        painter.setPen(QColor(255, 0, 0))  # Red color for arc
        painter.drawArc(center[0] - radius, center[1] - radius,
                        radius * 2, radius * 2, 90 * 16, int(angle * 16))

        painter.setPen(QColor(0, 0, 0))  # Black color for text
        text = f"{float(progress * 100)}%"
        text_rect = painter.boundingRect(0, 0, 0, 0, Qt.AlignCenter, text)
        text_width = text_rect.width()
        text_height = text_rect.height()

        # Center the text
        painter.drawText(center[0] - text_width // 2, center[1] - text_height // 2, text)

    def update_image(self):
        # Create a new QImage to paint on it
        img_copy = QImage(self.pixmap.size(), QImage.Format_RGB888)
        img_copy.fill(QColor(255, 255, 255))  # Fill with white background

        painter = QPainter(img_copy)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw all the elements (bars and circles)
        self.draw_bar(painter, 24, self.memory, "Memory Usage")
        self.draw_bar(painter, 54, self.net_up_speed / 1024, "Net Up Speed")
        self.draw_bar(painter, 84, self.net_down_speed / 1024, "Net Down Speed")

        self.draw_circle(painter, self.cpu_percent / 100.0, 130, "CPU Percent")
        self.draw_circle(painter, self.cpu_freq / 1000.0, 230, "CPU Frequency")
        self.draw_circle(painter, self.cpu_temperature / 100.0, 330, "CPU Temperature")

        painter.end()
        return img_copy

    def update_progress(self):
        # Simulate the update of system stats here
        self.cpu_percent = (self.cpu_percent + 1) % 100
        self.cpu_freq = (self.cpu_freq + 10) % 4000
        self.cpu_temperature = (self.cpu_temperature + 1) % 100
        self.memory = (self.memory + 0.02) % 1  # 0 to 1
        self.net_up_speed = (self.net_up_speed + 50) % 1000  # KB/s
        self.net_down_speed = (self.net_down_speed + 50) % 1000  # KB/s

        img_copy = self.update_image()

        # Update the pixmap
        self.pixmap = QPixmap.fromImage(img_copy)
        self.label.setPixmap(self.pixmap)

    def show_image(self, img_copy):
        self.pixmap = QPixmap.fromImage(img_copy)
        self.label.setPixmap(self.pixmap)

    def run(self):
        self.show()

# Example usage:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_path = "D:/project/STM32F103/pyQt/UI_TEXT1.0/UI/res/3.5/swsw.png"  # Replace with your image path
    progress_bar = ProgressBar(image_path)
    progress_bar.run()
    sys.exit(app.exec_())
