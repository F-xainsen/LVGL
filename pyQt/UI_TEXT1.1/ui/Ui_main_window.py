# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\project\pyQt\UI_TEXT2.1\UI\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(776, 458)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(260, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(260, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_serial_refresh = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_serial_refresh.setAutoFillBackground(False)
        self.btn_serial_refresh.setStyleSheet("background-color: transparent;\n"
"border: none;")
        self.btn_serial_refresh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/refresh"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_serial_refresh.setIcon(icon)
        self.btn_serial_refresh.setObjectName("btn_serial_refresh")
        self.gridLayout_2.addWidget(self.btn_serial_refresh, 0, 2, 1, 1)
        self.cb_devices = QtWidgets.QComboBox(self.groupBox_2)
        self.cb_devices.setObjectName("cb_devices")
        self.gridLayout_2.addWidget(self.cb_devices, 0, 1, 1, 1)
        self.label_connect_state = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_connect_state.sizePolicy().hasHeightForWidth())
        self.label_connect_state.setSizePolicy(sizePolicy)
        self.label_connect_state.setMaximumSize(QtCore.QSize(20, 20))
        self.label_connect_state.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_connect_state.setStyleSheet("")
        self.label_connect_state.setText("")
        self.label_connect_state.setPixmap(QtGui.QPixmap(":/icon/disc"))
        self.label_connect_state.setScaledContents(True)
        self.label_connect_state.setAlignment(QtCore.Qt.AlignCenter)
        self.label_connect_state.setWordWrap(True)
        self.label_connect_state.setObjectName("label_connect_state")
        self.gridLayout_2.addWidget(self.label_connect_state, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.cb_baudrate = QtWidgets.QComboBox(self.groupBox_2)
        self.cb_baudrate.setObjectName("cb_baudrate")
        self.cb_baudrate.addItem("")
        self.cb_baudrate.addItem("")
        self.cb_baudrate.addItem("")
        self.cb_baudrate.addItem("")
        self.cb_baudrate.addItem("")
        self.cb_baudrate.addItem("")
        self.cb_baudrate.addItem("")
        self.gridLayout_2.addWidget(self.cb_baudrate, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.btn_open_device = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_open_device.setObjectName("btn_open_device")
        self.gridLayout_2.addWidget(self.btn_open_device, 2, 1, 1, 2)
        self.toolButton = QtWidgets.QToolButton(self.groupBox_2)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_2.addWidget(self.toolButton, 1, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.edit_log = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.edit_log.setReadOnly(True)
        self.edit_log.setObjectName("edit_log")
        self.verticalLayout_2.addWidget(self.edit_log)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_hex = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_hex.setChecked(True)
        self.cb_hex.setObjectName("cb_hex")
        self.horizontalLayout_2.addWidget(self.cb_hex)
        self.btn_clear = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_clear.setObjectName("btn_clear")
        self.horizontalLayout_2.addWidget(self.btn_clear)
        self.cb_recv = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_recv.setChecked(True)
        self.cb_recv.setObjectName("cb_recv")
        self.horizontalLayout_2.addWidget(self.cb_recv)
        self.cb_send = QtWidgets.QCheckBox(self.groupBox_2)
        self.cb_send.setChecked(True)
        self.cb_send.setObjectName("cb_send")
        self.horizontalLayout_2.addWidget(self.cb_send)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5.addWidget(self.groupBox_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.screenflipping = QtWidgets.QComboBox(self.centralwidget)
        self.screenflipping.setObjectName("screenflipping")
        self.screenflipping.addItem("")
        self.screenflipping.addItem("")
        self.horizontalLayout_3.addWidget(self.screenflipping)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.fileEdit = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fileEdit.setFont(font)
        self.fileEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fileEdit.setReadOnly(False)
        self.fileEdit.setObjectName("fileEdit")
        self.verticalLayout.addWidget(self.fileEdit)
        self.sizeEdit = QtWidgets.QLabel(self.centralwidget)
        self.sizeEdit.setMinimumSize(QtCore.QSize(121, 21))
        self.sizeEdit.setMaximumSize(QtCore.QSize(121, 21))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(11)
        self.sizeEdit.setFont(font)
        self.sizeEdit.setObjectName("sizeEdit")
        self.verticalLayout.addWidget(self.sizeEdit)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.open_image = QtWidgets.QPushButton(self.centralwidget)
        self.open_image.setMinimumSize(QtCore.QSize(0, 30))
        self.open_image.setObjectName("open_image")
        self.layout.addWidget(self.open_image)
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setMinimumSize(QtCore.QSize(0, 30))
        self.run_button.setObjectName("run_button")
        self.layout.addWidget(self.run_button)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setMinimumSize(QtCore.QSize(0, 30))
        self.stop_button.setObjectName("stop_button")
        self.layout.addWidget(self.stop_button)
        self.horizontalLayout_4.addLayout(self.layout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.view = QtWidgets.QLabel(self.centralwidget)
        self.view.setMinimumSize(QtCore.QSize(240, 200))
        self.view.setMaximumSize(QtCore.QSize(240, 260))
        self.view.setText("")
        self.view.setAlignment(QtCore.Qt.AlignCenter)
        self.view.setObjectName("view")
        self.horizontalLayout.addWidget(self.view)
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setMinimumSize(QtCore.QSize(240, 260))
        self.info_label.setMaximumSize(QtCore.QSize(240, 260))
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(11)
        self.info_label.setFont(font)
        self.info_label.setText("")
        self.info_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.info_label.setObjectName("info_label")
        self.horizontalLayout.addWidget(self.info_label)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 108, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.label.raise_()
        self.screenflipping.raise_()
        self.fileEdit.raise_()
        self.sizeEdit.raise_()
        self.info_label.raise_()
        self.view.raise_()
        self.groupBox_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 776, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.cb_baudrate.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "串口设置"))
        self.label_6.setText(_translate("MainWindow", "设备："))
        self.cb_baudrate.setCurrentText(_translate("MainWindow", "115200"))
        self.cb_baudrate.setItemText(0, _translate("MainWindow", "4800"))
        self.cb_baudrate.setItemText(1, _translate("MainWindow", "9600"))
        self.cb_baudrate.setItemText(2, _translate("MainWindow", "14400"))
        self.cb_baudrate.setItemText(3, _translate("MainWindow", "115200"))
        self.cb_baudrate.setItemText(4, _translate("MainWindow", "128000"))
        self.cb_baudrate.setItemText(5, _translate("MainWindow", "230400"))
        self.cb_baudrate.setItemText(6, _translate("MainWindow", "256000"))
        self.label_7.setText(_translate("MainWindow", "波特率："))
        self.btn_open_device.setText(_translate("MainWindow", "打开串口"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.edit_log.setPlaceholderText(_translate("MainWindow", "收发日志显示区"))
        self.cb_hex.setText(_translate("MainWindow", "Hex"))
        self.btn_clear.setText(_translate("MainWindow", "清空日志"))
        self.cb_recv.setText(_translate("MainWindow", "收"))
        self.cb_send.setText(_translate("MainWindow", "发"))
        self.label.setText(_translate("MainWindow", " 屏幕翻转"))
        self.screenflipping.setItemText(0, _translate("MainWindow", "0°"))
        self.screenflipping.setItemText(1, _translate("MainWindow", "180°"))
        self.sizeEdit.setText(_translate("MainWindow", "Size：0    B"))
        self.open_image.setText(_translate("MainWindow", "选择图形"))
        self.run_button.setText(_translate("MainWindow", "运行"))
        self.stop_button.setText(_translate("MainWindow", "停止"))
from ui import resource_rc
