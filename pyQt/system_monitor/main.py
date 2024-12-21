import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from views.main_view import MainWindow

if __name__ == '__main__':
    # 1.创建应用程序
    app = QApplication(sys.argv)
    # 2.创建窗口
    window = MainWindow()
    # 3.显示窗口
    window.show()
    # 4.等待窗口停止
    sys.exit(app.exec())
