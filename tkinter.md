'''python
windows 自带系统版本
'''
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import ctypes

class ExamCountdown:
    def __init__(self, master):
        self.master = master
        self.master.title("专升本考试倒计时")

        self.exam_date_label = ttk.Label(master, text="考试日期（格式：YYYY-MM-DD）:")
        self.exam_date_label.grid(row=0, column=0, padx=10, pady=10)

        self.exam_date_entry = ttk.Entry(master)
        self.exam_date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.result_label = ttk.Label(master, text="")
        self.result_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.calculate_button = ttk.Button(master, text="计算天数", command=self.calculate_days)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_days(self):
        exam_date_str = self.exam_date_entry.get()

        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
            current_date = datetime.now()

            if exam_date > current_date:
                days_left = (exam_date - current_date).days
                result_text = f"距离考试还有 {days_left} 天。"
                self.result_label.config(text=result_text)

                # 在Windows上显示桌面通知
                if ctypes.windll.user32.MessageBoxW(0, f"距离考试还有 {days_left} 天。", "专升本考试倒计时", 1) == 1:
                    pass  # 用户点击了通知

            else:
                self.result_label.config(text="请输入有效的未来日期。")
        except ValueError:
            self.result_label.config(text="日期格式错误，请使用YYYY-MM-DD格式。")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamCountdown(root)

    # 设置默认考试日期为2024-04-01
    app.exam_date_entry.insert(0, "2024-04-01")

    # 计算初始天数
    app.calculate_days()

    # 隐藏主窗口
    root.iconify()

    # 开始主循环
    root.mainloop()
#其他库文件版本
from tkinter import Tk, Label, Entry, Button, StringVar
from datetime import datetime, timedelta
from plyer import notification
import threading


class ExamCountdown:
    def __init__(self, master):
        self.master = master
        self.master.title("专升本考试倒计时")

        self.exam_date_label = Label(master, text="考试日期（格式：YYYY-MM-DD）:")
        self.exam_date_label.grid(row=0, column=0, padx=10, pady=10)

        self.exam_date_entry = Entry(master)
        self.exam_date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.result_label = Label(master, text="")
        self.result_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.calculate_button = Button(master, text="计算天数", command=self.calculate_days)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_days(self):
        exam_date_str = self.exam_date_entry.get()

        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
            current_date = datetime.now()

            if exam_date > current_date:
                days_left = (exam_date - current_date).days
                result_text = f"距离考试还有 {days_left} 天。"
                self.result_label.config(text=result_text)

                # 启动后台通知线程
                threading.Thread(target=self.show_notification, args=(days_left,), daemon=True).start()

            else:
                self.result_label.config(text="请输入有效的未来日期。")
        except ValueError:
            self.result_label.config(text="日期格式错误，请使用YYYY-MM-DD格式.")

    def show_notification(self, days_left):
        notification_title = "专升本考试倒计时"
        notification_message = f"距离考试还有 {days_left} 天。"

        # 显示桌面通知
        notification.notify(
            title=notification_title,
            message=notification_message,
            timeout=10  # 通知显示时间，单位为秒
        )


if __name__ == "__main__":
    root = Tk()
    app = ExamCountdown(root)

    # 设置默认考试日期为2024-04-01
    app.exam_date_entry.insert(0, "2024-04-01")

    # 计算初始天数
    app.calculate_days()

    # 隐藏主窗口
    root.iconify()

    # 开始主循环
    root.mainloop()
