import cv2
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import tkinter as tk
from tkinter import filedialog, simpledialog
from threading import Lock

# 函数：获取视频分辨率
def get_video_resolution(video_path, timeout):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return (width, height)

# 函数：处理每一行
def process_line(line, output_file, order_list, valid_count, invalid_count, total_lines, min_resolution, timeout, process_lock):
    parts = line.strip().split(',')
    if '#genre#' in line:
        with process_lock:
            output_file.write(line)
            print(f"已写入genre行：{line.strip()}")
    elif len(parts) == 2:
        channel_name, channel_url = parts
        resolution = get_video_resolution(channel_url, timeout)
        if resolution and resolution[1] >= min_resolution:
            with process_lock:
                output_file.write(f"{channel_name}[{resolution[1]}p],{channel_url}\n")
                order_list.append((channel_name, resolution[1], channel_url))
                valid_count[0] += 1
                print(f"Channel '{channel_name}' accepted with resolution {resolution[1]}p at URL {channel_url}.")
        else:
            invalid_count[0] += 1
    with process_lock:
        print(f"有效: {valid_count[0]}, 无效: {invalid_count[0]}, 总数: {total_lines}, 进度: {(valid_count[0] + invalid_count[0]) / total_lines * 100:.2f}%")

# 函数：多线程工作
def worker(task_queue, output_file, order_list, valid_count, invalid_count, total_lines, min_resolution, timeout, process_lock):
    while True:
        try:
            line = task_queue.get(timeout=1)
            process_line(line, output_file, order_list, valid_count, invalid_count, total_lines, min_resolution, timeout, process_lock)
        except Queue.Empty:
            break
        finally:
            task_queue.task_done()

# 函数：启动程序
def start_program(root, source_file_path, min_resolution, timeout, num_threads):
    order_list = []
    valid_count = [0]
    invalid_count = [0]
    task_queue = Queue()
    process_lock = Lock()

    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        lines = source_file.readlines()

    output_file_path = simpledialog.askstring("输出文件名", "请输入输出文件名（不含扩展名）：", parent=root)
    if not output_file_path:
        return

    with open(output_file_path + '.txt', 'w', encoding='utf-8') as output_file:
        # 创建线程池
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 创建并启动工作线程
            for _ in range(num_threads):
                executor.submit(worker, task_queue, output_file, order_list, valid_count, invalid_count, len(lines), min_resolution, timeout, process_lock)

            # 将所有行放入队列
            for line in lines:
                task_queue.put(line)

            # 等待队列中的所有任务完成
            task_queue.join()

    print(f"任务完成，有效频道数：{valid_count[0]}, 无效频道数：{invalid_count[0]}, 总频道数：{len(lines)}")

# GUI界面
class App:
    def __init__(self, root):
        self.root = root
        root.title("视频处理程序")

        # 创建输入框和按钮
        self.source_label = tk.Label(root, text="选择源文件:")
        self.source_label.pack()

        self.source_button = tk.Button(root, text="浏览", command=self.load_source_file)
        self.source_button.pack()

        self.timeout_label = tk.Label(root, text="视频超时时间(秒):")
        self.timeout_label.pack()

        self.timeout_entry = tk.Entry(root)
        self.timeout_entry.pack()

        self.resolution_label = tk.Label(root, text="最低分辨率:")
        self.resolution_label.pack()

        self.resolution_entry = tk.Entry(root)
        self.resolution_entry.pack()

        self.threads_label = tk.Label(root, text="线程数:")
        self.threads_label.pack()

        self.threads_entry = tk.Entry(root)
        self.threads_entry.pack()

        self.start_button = tk.Button(root, text="开始", command=self.run_program)
        self.start_button.pack()

    def load_source_file(self):
        file_path = filedialog.askopenfilename(title="选择源文件", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.source_button.config(text=file_path)

    def run_program(self):
        source_file_path = self.source_button.cget("text")
        try:
            timeout = int(self.timeout_entry.get())
            min_resolution = int(self.resolution_entry.get())
            num_threads = int(self.threads_entry.get())
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数字")
            return

        if not source_file_path or timeout <= 0 or min_resolution <= 0 or num_threads <= 0:
            tk.messagebox.showerror("错误", "所有输入框都必须填写有效值")
            return

        start_program(self.root, source_file_path, min_resolution, timeout, num_threads)
   
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
