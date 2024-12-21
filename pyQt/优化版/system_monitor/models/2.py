# main.py
import threading
import queue
import time
import monitor as sm
import data_provider as dp

def system_monitor_thread(data_queue: queue.Queue):
    monitor = sm.SystemMonitor(data_queue)
    while True:
        monitor.update_all()
        time.sleep(1)  # 每秒更新一次数据

def image_update_thread(data_queue: queue.Queue):
    dp.update_image_from_queue(data_queue)

if __name__ == "__main__":
    data_queue = queue.Queue()  # 创建一个队列用于传递数据

    # 启动系统监控线程
    monitor_thread = threading.Thread(target=system_monitor_thread, args=(data_queue,), daemon=True)
    monitor_thread.start()

    # 启动图像更新线程
    image_thread = threading.Thread(target=image_update_thread, args=(data_queue,), daemon=True)
    image_thread.start()

    # 主线程保持运行
    while True:
        time.sleep(1)  # 主线程什么都不做，只是保持程序运行
