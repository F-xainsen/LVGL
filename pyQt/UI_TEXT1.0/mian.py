import sys
import os
import serial
from PIL import Image
import math
import binascii
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import struct
import serial.tools.list_ports
import multiprocessing

from UI.Ui_main_window import Ui_MainWindow
from CPU.get_cpu import GetCPUInfo

from drivers.driver_serial import *
from common.protocol import *


    
################################################################################
# this model generate by chatgpt
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
        
        self.cur_serial_device: SerialDevice = None
        self.data_block = None
          
        #1.获取用户旋转屏幕和主题
        screen = self.ui.screenflipping.currentText()   
        theme  = self.ui.theme.currentText()
        print(f"screen:{screen}, theme:{theme}")
        
    
        
        # 创建 GetCPUInfo 实例
        self.cpu_thread = GetCPUInfo()
        self.running = False
        
        self.monitor = SystemMonitor(
            cpu_usage=None,
            cpu_frequency=None,
            cpu_temperature=0,
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
        self.update_serial_port()
        # self.on_btn_open_image_clicked()
        
       
        
    def init_ui(self):
        
        self.ui.screenflipping.currentText()
        self.ui.theme.currentText()
        
        # 创建run按钮
        # self.run_button = QPushButton("运行", self)
        self.ui.run_button.clicked.connect(self.on_run)
        self.ui.stop_button.clicked.connect(self.on_stop)
        
        # 绑定串口更新按钮
        self.ui.update_button.clicked.connect(self.update_serial_port)
    
    
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
        data = [[self.monitor.cpu_usage,"cpu_usage"], 
                [self.monitor.cpu_frequency,"cpu_frequency"], 
                [self.monitor.cpu_temperature,"cpu_temperature"], 
                [self.monitor.gpu_name,"gpu_name"], 
                [self.monitor.gpu_temp,"gpu_temp"], 
                [self.monitor.gpu_usage,"gpu_usage"], 
                [self.monitor.memory_usage,"memory_usage"], 
                [self.monitor.upload_speed,"upload_speed"], 
                [self.monitor.download_speed,"download_speed"]
            ]
        # 组装数据为字符串
        formatted_data = []
        for value, name in data:
            formatted_data.append(f"{name}:{value}")

        # 将数据拼接成最终的发送字符串
        send_string = ";".join(formatted_data)

        # 调用发送函数
        #self.send_to_device(send_string)
        #print(f"发送到下位机的数据: {send_string}")
        #图片传输完成后，发送数据到下位机
        if self.data_block is None:
            self.send_to_device(bytes(send_string,encoding="utf-8"))
            # print(f"发送到下位机的数据: {send_string}")
        # convert_data = [self.float_to_hex_big_endian(val, 2) for val in data]
        # self.send_to_device(convert_data)

    
    @pyqtSlot()
    def on_btn_open_image_clicked(self):
        """
        1. 打开文件对话框，允许选择res文件夹下的图片文件。
        2. 如果选择了文件，加载并显示图片。
        3. 如果没有选择文件或文件不是有效的图片，显示错误提示。
        """
        # 获取当前工作目录，假设 res 文件夹在当前目录下
        res_folder = os.path.join(os.getcwd(),"UI", "res","3.5")

        # # 打开文件选择对话框，默认显示res文件夹，只允许选择图片文件
        file_name = QFileDialog.getOpenFileName(
            self, "打开图片", res_folder, "图片文件 (*.png)"
        )
        # file_name = [f for f in os.listdir(res_folder) if f.endswith('.png')]

        # file_name = ["D:/project/pyQt/UI_TEXT2.0/UI/res/3.5/swsw.png"]
        if not file_name[0]:
            # 用户没有选择文件
            self.statusBar().showMessage("没有选择任何文件", 1000)
            return
               
        # 显示选择的文件名
        self.ui.fileEdit.setText(file_name[0])
        # 显示图片大小
        # self.ui.sizeEdit.setText(f"{os.path.getsize(file_name[0])} bytes")
        
        print(file_name[0])
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
            print(f"图片尺寸：{width}x{height}像素")
            
            # 强制调整图片大小
            pixmap = pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
            print(f"图片缩放尺寸：{pixmap.width()}x{pixmap.height()}像素")
            
            # 在界面上显示图片
            # self.ui.view.setPixmap(modified_pixmap)
            self.ui.view.setPixmap(QPixmap.fromImage(pixmap))
            self.ui.view.setScaledContents(True)  # 图片按比例缩放
            self.statusBar().showMessage(f"成功加载图片：{file_name}", 1000)

            rgb565_data = self.convert_to_rgb565(pixmap)
            print(f"RGB565数据长度：{len(rgb565_data)} bytes")
            if rgb565_data is None:
                print("图片处理失败或返回空数据！")
                return
               
            
            # 分块发送RGB565数据
            block_size = 640  # 每个数据包的大小为64字节
            num_blocks = len(rgb565_data) // block_size + (1 if len(rgb565_data) % block_size > 0 else 0)

            # 分块并发送
            for i in range(num_blocks):
                start_index = i * block_size
                end_index = min((i + 1) * block_size, len(rgb565_data))
                data_block = rgb565_data[start_index:end_index]
                self.send_to_device(data_block)
                # print(f"发送第{i+1}/{num_blocks}个数据包，大小：{len(data_block)} bytes")
            print(F"打印数据：{rgb565_data}")    
            
        except Exception as e:
            # 如果加载过程中发生任何错误，弹出警告框
            QMessageBox.warning(self, "打开失败", f"发生错误：{str(e)}") 
            
    
        

    def convert_24bit_to_32bit(self, image_path, output_path):
        # 打开图片
        img = Image.open(image_path)
        
        # 如果图像是24位RGB图像，转换为32位RGBA图像
        if img.mode == 'RGB':
            img = img.convert('RGBA')
        else:
            img = img.convert('RGBA')
        
        # 保存转换后的32位图像
        img.save(output_path)



            
    def convert_to_rgb565(self, pixmap):
        """
        将QImage图像转换为RGB565格式
        """


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
        
        if pixmap.isNull():
            return None

        # 获取图片的像素数据
        width, height = image.width(), image.height()
        

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
                # print(f"RGB565数据: {rgb565_data[y, x]}")
        # 将rgb565_data转换为2字节，高字节在前，低字节在后
        rgb565_gight = rgb565_data >> 8
        rgb565_data = rgb565_data << 8
        #将高低字节合并
        rgb565_data = rgb565_data | rgb565_gight

        # 转换为字节数据
        rgb565_bytes = rgb565_data.tobytes()
        return rgb565_bytes
        # #转化为16进制字符串
        # hex_data = binascii.hexlify(rgb565_bytes)
        # hex_data = hex_data.upper()  # 转换为大写
        # print(f"转换后的16进制数据: {hex_data}")
        
        # return hex_data
    
    # def convert_to_rgb565(image_path, width=320, height=240):
    #     try:
    #         # 打开图片并缩放为320x240
    #         img = Image.open(image_path)
    #         img = img.resize((width, height))

    #         # 转换为 RGB 模式
    #         img = img.convert('RGB')

    #         # 创建一个字节数组存储RGB565数据
    #         rgb565_data = bytearray()

    #         for y in range(height):
    #             for x in range(width):
    #                 r, g, b = img.getpixel((x, y))

    #                 # 将 RGB 转换为 RGB565
    #                 r = (r >> 3) & 0x1F     # 5 bits for red
    #                 g = (g >> 2) & 0x3F     # 6 bits for green
    #                 b = (b >> 3) & 0x1F     # 5 bits for blue

    #                 # 组装为 RGB565（高位在前）
    #                 rgb565 = (r << 11) | (g << 5) | b
    #                 # 将 RGB565 转换为两个字节并添加到数据列表
    #                 rgb565_data.extend(struct.pack('>H', rgb565))  # Big-endian format (高位在前)

    #         return rgb565_data
    #     except Exception as e:
    #         print(f"图片处理失败: {e}")
    #     return None
    
    
    def get_selected_serial_port(self):
        """ 获取用户选择的串口 """
        selected_port = self.ui.serial_port_combobox.currentText()
        # serial_device = self.ui.serial_port_combobox.currentData()
        # self.update_serial_device(serial_device)
        return selected_port if selected_port != "没有找到串口设备1" else None

    def get_available_ports(self):
        """ 获取所有可用的串口设备 """
        ports = serial.tools.list_ports.comports()
        # return [port.device for port in ports]
        available_ports = []
        for port in ports:
            available_ports.append(port.device)
            print(f"串口: {port.device}, 描述: {port.description}")
            
        return available_ports

    @pyqtSlot()
    def update_serial_port(self):
        """ 更新串口选择框 """
        self.ui.serial_port_combobox.clear()  # 清空现有选项
        available_ports = self.get_available_ports()
        if available_ports:
            self.ui.serial_port_combobox.addItems(available_ports)  # 更新串口列表
        else:
            self.ui.serial_port_combobox.addItem("没有找到串口设备2")
        print(f"更新串口列表: {available_ports}")

        # self.cur_serial_device = serial_device
        
    def send_to_device(self, data):
        
        # 获取当前选中的串口
        serial_port = self.get_selected_serial_port()
        
        # 检查串口是否有效
        if serial_port is None or serial_port == "没有找到串口设备3":
            self.statusBar().showMessage("请先扫描设备.", 5000)
            return  # 串口无效，直接返回
        
        try:      
            baud_rate = 115200    # 波特率
            ser = serial.Serial(serial_port, baud_rate, timeout=1)

            # # 遍历数据元组，转换为float并打包为字节数据
            # byte_data = b''  # 初始化字节数据
            # for item in data:
            #     if isinstance(item, (list, np.ndarray)):  # 如果 item 是列表或数组
            #         # 递归处理 item 中的元素
            #         for sub_item in item:
            #             try:
            #                 byte_data += struct.pack('f', float(sub_item))  # 转换每个子项为float并打包
            #             except ValueError:
            #                 print(f"跳过不能转换为浮动数值的项: {sub_item}")
            #                 continue  # 跳过不能转换为浮动数值的项
            #     else:
            #         try:
            #             byte_data += struct.pack('f', float(item))  # 转换单个标量为float并打包
            #         except ValueError:
            #             print(f"跳过不能转换为浮动数值的项: {item}")
            #             continue  # 跳过不能转换为浮动数值的项
            
            # self.cur_serial_device.write(data)
            # 发送数据
            ser.write(data)
        
            # # 等待回应，读取下位机的回应数据（假设回应是以字节流的形式返回的）
            # response = ser.readline()  # 假设下位机的回应是以换行符结束的
            # print(f"接收到回应: {response}")
            # if response:
                # print(f"接收到回应: {response.decode('utf-8')}")
            #     # 这里可以根据回应内容来做进一步的处理
            #     self.handle_response(response.decode('utf-8'))
            # else:
            #     print("没有接收到回应")
                
            # 关闭串口
            ser.close()
            # print("数据已成功发送给下位机")
            
        except PermissionError as e:
            self.handle_serial_error(f"串口 {serial_port} 权限错误: {str(e)}")
        except serial.SerialException as e:
            self.handle_serial_error(f"串口 {serial_port} 打开失败: {str(e)}")
        except Exception as e:
            self.handle_serial_error(f"发送数据时发生错误: {str(e)}")
            
    def handle_serial_error(self, error_message):
        """ 处理串口错误信息，只提示一次 """
        if not self.serial_error_flag:
            self.serial_error_flag = True  # 设置标志，表示已提示错误
            QMessageBox.warning(self, "串口错误", error_message)

    def handle_response(self, response):
        """
        处理从下位机接收到的回应
        """
        print(f"处理接收到的回应: {response}")
        # 例如，如果回应是某些操作成功或失败的信息，可以在UI上显示
        if "SUCCESS" in response:
            self.statusBar().showMessage("数据传输成功", 1000)
        else:
            self.statusBar().showMessage(f"传输失败: {response}", 1000)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    # 1.创建应用程序
    app = QApplication(sys.argv)
    # 2.创建窗口
    window = MainWindow()
    # 3.显示窗口
    window.show()
    # 4.等待窗口停止
    sys.exit(app.exec_())