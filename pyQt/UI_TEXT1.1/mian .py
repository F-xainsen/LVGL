import sys
import os
import serial
import math
import binascii
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import struct
import serial.tools.list_ports

from ui.Ui_main_window import Ui_MainWindow
from CPU.get_cpu import GetCPUInfo

from common.protocol import *
from common.utils import *
from common.qt_worker import Worker
from drivers.driver_serial import *
"""
数据格式

功能码 + 数据
================发送===============
target: F0 00 00
    cpu_usage: E0 00 00 00 00 00
    cpu_freq: E0 01 00 00 00 00
    cpu_temp: E0 02 00 00 00 00
    gpu_name: E0 03 00 00 00 00
    gpu_temp: E0 04 00 00 00 00
    gpu_usage: E0 05 00 00 00 00
    mem_usage: E0 06 00 00 00 00
    up_s: E0 07 00 00 00 00
    dw_s: E0 08 00 00 00 00

================接收===============
current        : B0 00 00
kp + ki + kd   : B1 00 00 00 00 FF FF FF FF 00 00 00 00

"""
SEND_KEY_MAP = {"info": 0xE0, "target": 0xF0}


class SystemMonitor:
    def __init__(self, cpu_usage, cpu_frequency, cpu_temperature, gpu_name, gpu_temp, gpu_usage, memory_usage, upload_speed, download_speed):
        # CPU attributes
        self.cpu_usage = cpu_usage  # in percentage
        self.cpu_frequency = cpu_frequency  # in MHz or GHz
        self.cpu_temperature = cpu_temperature  # in Celsius
        
        # GPU attributes
        self.gpu_name = gpu_name
        self.gpu_temp = gpu_temp  # in Celsius
        self.gpu_usage = gpu_usage  # in percentage
        
        # Memory attributes
        self.memory_usage = memory_usage  # in percentage or GB
        
        # Network attributes
        self.upload_speed = upload_speed  # in Mbps
        self.download_speed = download_speed  # in Mbps



    def __str__(self):        
        return (f"System Monitor:\n"
                f"CPU占用率: {self.cpu_usage}%\n"
                f"CPU主频: {self.cpu_frequency} GHz\n"
                f"CPU温度: {self.cpu_temperature} °C\n"
                f"GPU: {self.gpu_name}\n"
                f"GPU温度: {self.gpu_temp} °C\n"
                f"GPU占用率: {self.gpu_usage}%\n"
                f"内存占用率: {self.memory_usage}%\n"
                f"上传速度: {self.upload_speed if self.upload_speed is not None else 0.0:.2f} Mbps\n"
                f"下传速度: {self.download_speed if self.download_speed is not None else 0.0:.2f} Mbps")
    
################################################################################

class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        #加载UI内容
        self.ui.setupUi(self)
        #初始化UI
        self.init_ui()
        self.ui.open_image.clicked.connect(self.on_btn_open_image_clicked)
        
        # 工作线程为None
        self.cur_serial_device: SerialDevice = None
        self.refresh_worker: Worker = None
          
        #1.获取用户旋转屏幕
        screen = self.ui.screenflipping.currentText()   
        print(f"screen:{screen}")
        
        # 串口刷新按钮
        self.refresh_serial_devices()
        
        # 创建 GetCPUInfo 实例
        self.cpu_thread = GetCPUInfo()
        self.running = False
        
        self.monitor = SystemMonitor(
            cpu_usage=None,
            cpu_frequency=None,
            cpu_temperature=None,
            gpu_name=None,
            gpu_temp=None,
            gpu_usage=None,
            memory_usage=None,
            upload_speed=None,
            download_speed=None,  
        )

        # 初始化串口错误标志
        self.serial_error_flag = False

        # 连接信号到槽函数，用于更新UI
        self.cpu_thread.cpu_info_signal.connect(self.update_cpu_info)
        self.cpu_thread.gpu_info_signal.connect(self.update_gpu_info)
        self.cpu_thread.memory_info_signal.connect(self.update_memory_info)
        self.cpu_thread.network_info_signal.connect(self.update_network_info)
        # # 启动线程
        self.cpu_thread.start()
        
        # 创建一个定时器，在主线程中启动
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_run)  # 定时调用 on_run 方法
        self.timer.start(100)  # 每500ms触发一次，更新硬件信息
        
        # 初始化停止标志
        self.cpu_thread.stop_signal.connect(self.on_stop)
        
    #################################################################################
    def on_slider_target_valueChanged(self, value):
        # 构建字节数组，首字节为0xF0, value用两个字节表示
        # data = bytes([0xF0, value >> 8, value & 0xFF])
        self.dialog.ui.rp_pid.update_target(value)
        if self.ui.actionEnterprise.isChecked():
            data = pack_protocol_data_with_checksum(SEND_KEY_MAP["target"], value)
        else:
            data = pack_protocol_data(SEND_KEY_MAP["target"], value)
    
        msg = f"设置目标值：{value} -> {decode_to_hex_str(data)}"
        # 打印字节数组
        # print(msg)
        
        if self.cur_serial_device is None:
            self.statusBar().showMessage("请先打开串口.", 3000)
            return
        
        self.statusBar().showMessage(msg, 3000)
        self.cur_serial_device.write(data)
        # 添加到日志
        self.append_send_log(data)
        
    @pyqtSlot()
    def on_btn_clear_clicked(self):
        self.ui.edit_log.clear()
        
    def append_send_log(self, content):
        if not self.ui.cb_send.isChecked():
            return
        
        # 根据是否勾选16进制，选择不同的显示方式
        if self.ui.cb_hex.isChecked():
            self.ui.edit_log.appendPlainText(f"🔵发->{decode_to_hex_str(content)}")
        else :
            # 将字节数组转成对应的字符串
            self.ui.edit_log.appendPlainText(f"🔵发->{decode_data(content)}")
            
            
    def update_ui(self):
        """
        根据连接状态更新UI
        :return:
        """
        if self.cur_serial_device is not None:
            # 修改图标
            self.ui.label_connect_state.setPixmap(QPixmap(":/icon/conn"))
            # 修改按钮文字
            self.ui.btn_open_device.setText("关闭串口")
        else:
            # 修改图标
            self.ui.label_connect_state.setPixmap(QPixmap(":/icon/disc"))
            # 修改按钮文字
            self.ui.btn_open_device.setText("打开串口")

    def close_serial_device(self):
        if self.cur_serial_device is not None:
            self.cur_serial_device.close()
            self.cur_serial_device = None

        self.update_ui()

    def on_refresh_serial_port_result(self, ports):
        self.ui.cb_devices.clear()
        # 添加每个元素1作为文本，元素0作为数据
        for port in ports:
            device, description = port
            self.ui.cb_devices.addItem(description, port)

        self.statusBar().showMessage(
            f"刷新完毕，{len(ports)} serial ports found.", 5000
        )

    def refresh_serial_devices(self):
        self.refresh_worker = Worker(scan_serial_ports)
        self.refresh_worker.signal_connect(
            result_handler=self.on_refresh_serial_port_result
        )
        self.refresh_worker.start()

    @pyqtSlot()
    def on_btn_serial_refresh_clicked(self):
        if self.refresh_worker is not None and self.refresh_worker.is_running:
            return

        self.refresh_serial_devices()

    def receive_data(self, worker: Worker):
        send_flag = True
        while worker.is_running:
            send_flag = True
            if self.cur_serial_device is None:
                break
            if not self.cur_serial_device.is_open():
                break
            
            data = None
            if self.is_enterprise_mode:
                data = self.cur_serial_device.read()
            else:
                data = self.cur_serial_device.readline()
                # if arr:
                #     d_len = len(arr)
                #     if d_len >= 2 and arr[d_len - 2] == 0x0d and arr[d_len - 1] == 0x0a:
                #         data = self.__buffer + arr
                #         self.__buffer = b''
                #     else:
                #         self.__buffer += arr
                #         send_flag = False
                    
            # print("data: ", data)
            if data is not None:
                if send_flag: worker.emit_msg(data)
            else:
                print("读取超时，或已断开！")
                break
        print("recv----------end")  
        
    def append_recv_log(self, data):
        if not self.ui.cb_recv.isChecked():
            return
        if self.ui.cb_hex.isChecked():
            hex_content = decode_to_hex_str(data)
            self.ui.edit_log.appendPlainText(f"🟩收->{hex_content}")
        else:
            normal_content = decode_data(data)
            self.ui.edit_log.appendPlainText(f"🟩收->{normal_content}")
            
    def open_serial_device(self, serial_device, baudrate):
        port, description = serial_device
        serial_device = SerialDevice(port, baudrate)
        success, msg = serial_device.open()
        if not success:
            self.statusBar().showMessage(f"设备{description}连接失败：{msg}", 3000)
            self.cur_serial_device = None
            return

        self.cur_serial_device = serial_device
        tip_msg = f"设备【{description}】连接成功."
        self.statusBar().showMessage(tip_msg, 3000)
        print(tip_msg)
        self.update_ui()
        
        self.is_pid_sync = False
        self.ui.label_sync_state.setText("未同步❌")
        self.ui.label_sync_time.setText(QDateTime.currentDateTime().toString("HH:mm:ss"))
        self.ui.label_sync_state_2.setText("未同步❌")
        self.ui.label_sync_time_2.setText(QDateTime.currentDateTime().toString("HH:mm:ss"))

        # 开启WorkerThread
        self.recv_worker = Worker(self.receive_data).signal_connect(
            msg_handler=self.on_serial_data_received,
            finished_handler=self.close_serial_device
        )
        self.recv_worker.start()
        
        
    @pyqtSlot()
    def on_btn_open_device_clicked(self):
        if self.cur_serial_device is not None:
            self.close_serial_device()
            return

        # check devices count
        if self.ui.cb_devices.count() == 0:
            self.statusBar().showMessage("请先扫描设备.", 5000)
            return

        # get selected device
        serial_device = self.ui.cb_devices.currentData()
        baudrate = int(self.ui.cb_baudrate.currentText())
        self.open_serial_device(serial_device, baudrate)

    def on_cb_hex_stateChanged(self, state):
        if state == Qt.Checked:
            self.ui.edit_log.clear()
            self.ui.edit_log.setPlaceholderText("Hex显示")
        else:
            self.ui.edit_log.clear()
            self.ui.edit_log.setPlaceholderText("ASCII显示")
            
            
     ##############################################################################################   
         
    def init_ui(self):
        
        self.ui.screenflipping.currentText()
        
        # 创建run按钮
        # self.run_button = QPushButton("运行", self)
        self.ui.run_button.clicked.connect(self.on_run)
        self.ui.stop_button.clicked.connect(self.on_stop)
        
        
    
    @pyqtSlot()
    def on_run(self):
        """点击Run按钮时启动获取硬件信息的子线程"""
        if not self.cpu_thread.isRunning():  # 判断线程是否已经在运行
            self.cpu_thread.start()  # 启动线程
            self.cpu_thread.running = True
            self.timer.start(200)
            print("开始获取信息")
        else:
            #print("子线程已经在运行")
            pass
            
      
           
    @pyqtSlot()
    def on_stop(self):
        """点击Stop按钮时停止获取信息"""
        self.cpu_thread.stop()  # 停止子线程
        self.running = False  # 设置停止标志
        self.timer.stop()
        
        print("停止获取信息")

    def update_info(self):
        return
        """每秒获取一次CPU信息并发送数据到下位机"""
        # 从get_cpu.py中获取硬件信息
        #cpu_usage, cpu_frequency,cpu_temperature = self.cpu_thread.get_cpu_info()
        cpu_usage, cpu_frequency,cpu_temperature = None,None,None
        gpu_name, gpu_temp, gpu_usage = self.cpu_thread.get_gpu_info()
        memory_usage = self.cpu_thread.get_memory_info()
        upload_speed, download_speed = self.cpu_thread.get_network_speed()
        
        cpu_usage = cpu_usage if cpu_usage is not None else 0
        cpu_frequency = cpu_frequency if cpu_frequency is not None else 0.0
        cpu_temperature = cpu_temperature if cpu_temperature is not None else 0.0
        gpu_name = gpu_name if gpu_name is not None else "未知"
        gpu_temp = gpu_temp if gpu_temp is not None else 0.0
        gpu_usage = gpu_usage if gpu_usage is not None else 0.0
        memory_usage = memory_usage if memory_usage is not None else 0.0
        upload_speed = upload_speed if upload_speed is not None else 0.0
        download_speed = download_speed if download_speed is not None else 0.0
        
        # 显示在UI标签上
        info_text = (
            f"CPU占用率: {cpu_usage}%\n"
            f"CPU主频: {cpu_frequency:.2f} GHz\n"
            f"CPU主频: {cpu_temperature:.2f}\n"       
            f"显卡: {gpu_name}\n温度: {gpu_temp}°C\n占用率: {gpu_usage}%\n"
            f"内存占用率: {memory_usage}%\n"
            f"上传速度: {upload_speed:.2f} MB/s\n下载速度: {download_speed:.2f} MB/s"
        )
        self.ui.info_label.setText(info_text)

        # 将数据和图片发送给下位机
        # 假设你已经有一个方法可以将数据传给下位机
        data = cpu_usage, cpu_frequency, gpu_name, gpu_temp, gpu_usage, memory_usage, upload_speed, download_speed
        self.send_to_device(data)
        
        ################################################################################

    @pyqtSlot(list)
    def update_cpu_info(self,data):
        self.monitor.cpu_usage, self.monitor.cpu_frequency, self.monitor.cpu_temperature = data
        self.update_ui()
        pass
    @pyqtSlot(list)
    def update_gpu_info(self,data):
        self.monitor.gpu_name, self.monitor.gpu_temp, self.monitor.gpu_usage = data
        self.update_ui()
        pass
    @pyqtSlot(list)
    def update_memory_info(self,data):
        [self.monitor.memory_usage] = data
        self.update_ui()
        pass
    @pyqtSlot(list)
    def update_network_info(self,data):
        self.monitor.upload_speed, self.monitor.download_speed = data
        self.update_ui()
        pass

    def update_ui(self):
        self.ui.info_label.setText(str(self.monitor))
        # 假设你已经有一个方法可以将数据传给下位机
        data = [self.monitor.cpu_usage, 
                self.monitor.cpu_frequency, 
                self.monitor.cpu_temperature, 
                self.monitor.gpu_name, 
                self.monitor.gpu_temp, 
                self.monitor.gpu_usage, 
                self.monitor.memory_usage, 
                self.monitor.upload_speed, 
                self.monitor.download_speed
            ]
        self.send_to_device(data)

    
    @pyqtSlot()
    def on_btn_open_image_clicked(self):
        """
        1. 打开文件对话框，允许选择res文件夹下的图片文件。
        2. 如果选择了文件，加载并显示图片。
        3. 如果没有选择文件或文件不是有效的图片，显示错误提示。
        """
        # 获取当前工作目录，假设 res 文件夹在当前目录下
        res_folder = os.path.join(os.getcwd(), "res","3.5")

        # 打开文件选择对话框，默认显示res文件夹，只允许选择图片文件
        file_name = QFileDialog.getOpenFileName(
            self, "打开图片", res_folder, "图片文件 (*.png)"
        )
        # file_name = [f for f in os.listdir(res_folder) if f.endswith('.png')]

        if not file_name[0]:
            # 用户没有选择文件
            self.statusBar().showMessage("没有选择任何文件", 1000)
            return
    
        # 显示选择的文件名
        self.ui.fileEdit.setText(file_name[0])
        # 显示图片大小
        self.ui.sizeEdit.setText(f"{os.path.getsize(file_name[0])} bytes")
        
        print(file_name[1])
        # 尝试加载并显示图片
        try:
            pixmap = QImage(file_name[0])
            if pixmap.isNull():
                # 如果加载的图片为空，显示错误消息
                QMessageBox.warning(self, "打开失败", "无法加载此图片，请检查文件格式")
                return
            
            # 计算图片的宽度和高度
            # 获取3.5英寸显示屏的宽度和高度，假设DPI为96
            width, height =320,240
            
            # 强制调整图片大小
            pixmap = pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
            # print(f"图片缩放尺寸：{pixmap.width()}x{pixmap.height()}像素")
            
            # 在界面上显示图片
            # self.ui.view.setPixmap(modified_pixmap)
            self.ui.view.setPixmap(QPixmap.fromImage(pixmap))
            self.ui.view.setScaledContents(True)  # 图片按比例缩放
            self.statusBar().showMessage(f"成功加载图片：{file_name}", 1000)

            rgb565_data = self.convert_to_rgb565(pixmap)
            
        except Exception as e:
            # 如果加载过程中发生任何错误，弹出警告框
            QMessageBox.warning(self, "打开失败", f"发生错误：{str(e)}") 
        #每64个字节发送一次数据块
        for i in range(0, len(rgb565_data), 640):
             data_block = rgb565_data[i:i + 640]
             self.send_to_device(data_block)       
        print(f"发送完成")
    
            
    def convert_to_rgb565(self, pixmap):
        """
        将QImage图像转换为RGB565格式
        """
        print(f"图片尺寸：{pixmap.width()}x{pixmap.height()}像素")
        # 获取图片的宽高
        width = pixmap.width()
        height = pixmap.height()

        # 转换为QImage并获取数据
        # 确保 pixmap 是 QPixmap 类型
        # 确保pixmap是QImage类型
        if isinstance(pixmap, QImage):
            image = pixmap
        elif isinstance(pixmap, QPixmap):
            image = pixmap.toImage()
        else:
            print("pixmap 既不是 QPixmap 也不是 QImage 类型，而是:", type(pixmap))
            return None  # 如果pixmap不是QImage或QPixmap类型，返回None
        

        # 创建一个空的numpy数组来存储RGB565数据
        rgb565_data = np.zeros((height, width), dtype=np.uint16)
        # print(f"rgb565_data 数组的形状: {rgb565_data.shape}")
        
        for y in range(height):
            for x in range(width):
                # 获取每个像素的颜色
                pixel = image.pixel(x, y)
                r = (pixel >> 16) & 0xFF
                g = (pixel >> 8) & 0xFF
                b = pixel & 0xFF

                # 将RGB转为RGB565
                r5 = (r >> 3) & 0x1F
                g6 = (g >> 2) & 0x3F
                b5 = (b >> 3) & 0x1F

                # 组合成RGB565格式并存储
                rgb565_data[y, x] = (r5 << 11) | (g6 << 5) | b5
            
        # print(f"rgb565_data 数组的形状: {rgb565_data.shape}")
        # print(f"rgb565_data 数组的类型: {rgb565_data.dtype}")

        # 转换为字节数组
        rgb565_bytes = rgb565_data.tobytes()
        # print(f"转换后的RGB565数据大小：{len(rgb565_bytes)} bytes")
        
        return rgb565_bytes
    
    def send_to_device(self, value):
        
        data = pack_protocol_data_with_checksum(SEND_KEY_MAP["target"], value)
        
        msg = f"设置目标值：{value} -> {decode_to_hex_str(data)}"

        if self.cur_serial_device is None:
            self.statusBar().showMessage("请先打开串口.", 3000)
            return
        
        self.statusBar().showMessage(msg, 3000)
        self.cur_serial_device.write(data)
        # 添加到日志
        self.append_send_log(data)
        
        # # 获取当前选中的串口
        # serial_port = self.ui.cb_devices()
        
        # # 检查串口是否有效
        # if serial_port is None or serial_port == "没有找到串口设备":
        #     QMessageBox.warning(self, "串口错误", "没有有效的串口设备，请选择正确的串口。")
        #     return  # 串口无效，直接返回
        
        # try:      
        #     baud_rate = 115200     # 波特率
        #     ser = serial.Serial(serial_port, baud_rate, timeout=1)

        #     # 遍历数据元组，转换为float并打包为字节数据
        #     byte_data = b''  # 初始化字节数据
        #     for item in data:
        #         if isinstance(item, (list, np.ndarray)):  # 如果 item 是列表或数组
        #             # 递归处理 item 中的元素
        #             for sub_item in item:
        #                 try:
        #                     byte_data += struct.pack('f', float(sub_item))  # 转换每个子项为float并打包
        #                 except ValueError:
        #                     print(f"跳过不能转换为浮动数值的项: {sub_item}")
        #                     continue  # 跳过不能转换为浮动数值的项
        #         else:
        #             try:
        #                 byte_data += struct.pack('f', float(item))  # 转换单个标量为float并打包
        #             except ValueError:
        #                 print(f"跳过不能转换为浮动数值的项: {item}")
        #                 continue  # 跳过不能转换为浮动数值的项
                    
            # # 打印数据的 16 进制表示形式
            # hex_data = binascii.hexlify(byte_data).decode('utf-8')
            # print(f"转换后的16进制数据: {hex_data}")
            
            # # 发送数据到下位机
            # try:
            #     print(f"准备发送数据：{byte_data}")
            #     ser.write(byte_data)
            #     print(f"发送数据: {byte_data}")
            # except Exception as e:
            #     print(f"发送数据时发生错误: {e}")


            # # 等待回应，读取下位机的回应数据（假设回应是以字节流的形式返回的）
            # response = ser.readline()  # 假设下位机的回应是以换行符结束的
            # if response:
            #     print(f"接收到回应: {response.decode('utf-8')}")
            #     # 这里可以根据回应内容来做进一步的处理
            #     self.handle_response(response.decode('utf-8'))
            #     print("数据已成功发送给下位机")
            # else:
            #     print("没有接收到回应")
                
            # # 将RGB565数据分块发送给下位机
            # # 这里假设数据块的大小是64字节，你可以根据需要调整
            # block_size = 64
            # for i in range(0, len(byte_data), block_size):
            #     data_block = byte_data[i:i + block_size]
            #     ser.write(data_block)  # 发送数据块
            # print(f"发送数据长度：{len(byte_data)}，发送数据块大小：{block_size},分块数量：{len(byte_data)//block_size}")
            
    #         # 关闭串口
    #         ser.close()
            
            
    #     except PermissionError as e:
    #         self.handle_serial_error(f"串口 {serial_port} 权限错误: {str(e)}")
    #     except serial.SerialException as e:
    #         self.handle_serial_error(f"串口 {serial_port} 打开失败: {str(e)}")
    #     except Exception as e:
    #         self.handle_serial_error(f"发送数据时发生错误: {str(e)}")
            
    # def handle_serial_error(self, error_message):
    #     """ 处理串口错误信息，只提示一次 """
    #     if not self.serial_error_flag:
    #         self.serial_error_flag = True  # 设置标志，表示已提示错误
    #         QMessageBox.warning(self, "串口错误", error_message)

    # def handle_response(self, response):
    #     """
    #     处理从下位机接收到的回应
    #     """
    #     print(f"处理接收到的回应: {response}")
    #     # 例如，如果回应是某些操作成功或失败的信息，可以在UI上显示
    #     if "SUCCESS" in response:
    #         self.statusBar().showMessage("数据传输成功", 1000)
    #     else:
    #         self.statusBar().showMessage(f"传输失败: {response}", 1000)

if __name__ == '__main__':
    # 1.创建应用程序
    app = QApplication(sys.argv)
    # 2.创建窗口
    window = MainWindow()
    # 3.显示窗口
    window.show()
    # 4.等待窗口停止
    sys.exit(app.exec())