from tkinter import messagebox
from tkinter import *
import os
import shutil
import subprocess


def clean_log():
    with os.scandir('C:/src/kafka_2.13-3.3.1/logs') as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)
    show()


def start_browser():
    subprocess.Popen("start /wait python browser.py", shell=True)


def start_producer():
    subprocess.Popen("start /wait python producer.py", shell=True)


def start_consumer():
    subprocess.Popen("start /wait python consumer.py", shell=True)


def train():
    subprocess.Popen("start /wait python pretrain.py", shell=True)


def show(title="Message", message="Done!"):
    messagebox.showinfo(title, message)


def create_dataset():
    subprocess.Popen("start /wait python create_dataset.py", shell=True)


def zoo():
    subprocess.Popen(
        "start /wait C:/src/kafka_2.13-3.3.1/bin/windows/zookeeper-server-start.bat C:/src/kafka_2.13-3.3.1/config/zookeeper.properties", shell=True)


def kafka():
    subprocess.Popen(
        "start /wait C:/src/kafka_2.13-3.3.1/bin/windows/kafka-server-start.bat C:/src/kafka_2.13-3.3.1/config/server.properties", shell=True)


app = Tk()
app.geometry("200x400")

# chạy zookeeper
b_zoo = Button(app, text="Chạy zookeeper", command=zoo)
b_zoo.pack()

# chạy kafka
b_zoo = Button(app, text="Chạy kafka server", command=kafka)
b_zoo.pack()

# Xóa log Kafka
b_clean_log = Button(app, text="Xóa log Kafka", command=clean_log)
b_clean_log.pack()

# Chạy trình duyệt
b_browser = Button(app, text="Khởi động trình duyệt", command=start_browser)
b_browser.pack()

# Stream dữ liệu
b_get_data = Button(app, text="Stream dữ liệu facebook",
                    command=start_producer)
b_get_data.pack()

# Xử lý stream
b_process = Button(app, text="Chạy Stream processing",
                   command=start_consumer)
b_process.pack()

# Pretrain
b_train = Button(app, text="Train mô hình", command=train)
b_train.pack()

# Tạo dataset
b_dataset = Button(app, text='Tạo dataset', command=create_dataset)
b_dataset.pack()

app.mainloop()
