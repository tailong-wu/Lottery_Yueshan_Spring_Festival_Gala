import tkinter as tk
from tkinter import ttk
import random
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os
from datetime import datetime
from PIL import Image, ImageTk

# 初始化参与者列表
participants = [str(i) for i in range(1, 801)]
# 已中奖者列表
winners = {
    "三等奖": [],
    "二等奖": [],
    "一等奖": []
}

current_round = "三等奖"
rounds = {
    "三等奖": 10,
    "二等奖": 5,
    "一等奖": 1
}

# 声明全局变量
countdown_button = None
confirm_button = None
cancel_button = None

def draw_lottery():
    global participants, winners, current_round, rounds, draw_button
    global current_round_label, winner_label, winners_label
    global countdown_button, confirm_button, cancel_button  # 声明为全局变量
    
    draw_button.config(state=DISABLED)  # 禁用抽奖按钮
    if not participants:
        result_label.config(text="所有参与者都已参与抽奖！")
        draw_button.config(state=DISABLED)  # 禁用抽奖按钮
        return
    if rounds[current_round] == 0:
        if current_round == "三等奖":
            current_round = "二等奖"
            result_label.config(text="三等奖抽奖结束，即将开始二等奖抽奖！")
        elif current_round == "二等奖":
            current_round = "一等奖"
            result_label.config(text="二等奖抽奖结束，即将开始一等奖抽奖！")
        elif current_round == "一等奖":
            result_label.config(text="所有奖项抽奖结束！")
            save_results()  # 在所有奖项抽奖结束后保存结果
            draw_button.config(state=DISABLED)  # 禁用抽奖按钮
            return
    else:
        # 随机选择一名中奖者
        winner = random.choice(participants)
        # 创建倒计时按钮
        countdown_button = tb.Button(root, text="10秒倒计时", command=lambda: start_countdown(winner))
        countdown_button.pack(pady=10)

        # 创建确认和废除按钮
        confirm_button = tb.Button(root, text="确认", command=lambda: confirm_winner(winner))
        confirm_button.pack(side=tk.LEFT, padx=10)
        cancel_button = tb.Button(root, text="废除", command=lambda: cancel_winner(winner))
        cancel_button.pack(side=tk.LEFT, padx=10)

        # 更新当前轮次标签
        current_round_label.config(text=f"本次 {current_round} 第 {rounds[current_round]} 轮")
        # 更新结果标签以显示正在抽奖
        result_label.config(text=f"正在进行 {current_round} 抽奖")
        # 更新中奖者标签以显示中奖者信息
        winner_label.config(text=f"中奖者: {winner}")
        # 更新已中奖者标签以显示已中奖者信息
        winners_label.config(text=f"{current_round} 已中奖者: {', '.join(winners[current_round])}")
        print(f"当前轮次: {current_round}, 中奖者: {winner}, 已中奖者: {winners[current_round]}")  # 调试信息

def start_countdown(winner):
    global countdown_button, confirm_button, cancel_button  # 声明为全局变量

    countdown_button.config(state=DISABLED)  # 禁用倒计时按钮

    def update_countdown(seconds):
        if seconds > 0:
            countdown_button.config(text=f"{seconds}秒倒计时")
            root.after(1000, update_countdown, seconds - 1)
        else:
            countdown_button.destroy()

    update_countdown(10)

def confirm_winner(winner):
    global confirm_button, cancel_button, draw_button  # 声明为全局变量

    countdown_button.destroy()
    cancel_button.destroy()
    confirm_button.destroy()
    # 确认该号码中奖，将其从参与者列表中移除
    winners[current_round].append(winner)
    participants.remove(winner)
    rounds[current_round] -= 1
    # 创建一个新的标签来显示当前轮次
    current_round_label.config(text=f"本次 {current_round} 第 {rounds[current_round]} 轮")
    # 更新结果标签以显示中奖者信息
    result_label.config(text=f"正在进行 {current_round} 抽奖")
    # 更新中奖者标签以显示中奖者信息
    winner_label.config(text=f"中奖者: {winner}")
    # 更新已中奖者标签以显示已中奖者信息
    winners_label.config(text=f"{current_round} 已中奖者: {', '.join(winners[current_round])}")
    print(f"当前轮次: {current_round}, 中奖者: {winner}, 已中奖者: {winners[current_round]}")  # 调试信息
    draw_button.config(state=NORMAL)  # 启用抽奖按钮

def cancel_winner(winner):
    global confirm_button, cancel_button  # 声明为全局变量
    countdown_button.destroy()
    confirm_button.destroy()
    cancel_button.destroy()

    # 重新设置中奖者文本为空
    winner_label.config(text=f"中奖者: ")

    # 重新进行抽奖
    draw_button.config(state=NORMAL)  # 启用抽奖按钮
    print(f"废除中奖者: {winner}")  # 调试信息

def save_results():
    # 获取当前时间作为文件名
    global winners, rounds
    print(winners)
    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = f"result/{now}.txt"

    # 如果 result 文件夹不存在，则创建
    if not os.path.exists("result"):
        os.makedirs("result")

    # 将抽奖结果写入文件
    with open(filename, "w", encoding="utf-8") as file:
        file.write("抽奖结果\n")
        for round, winners in winners.items():
            file.write(f"{round}:\n")
            for winner in winners:
                file.write(f"{winner} - {round}\n")
        print(f"抽奖结果已保存到文件: {filename}")  # 调试信息

def resize_image(event):
    global background_image, background_photo
    new_width = event.width
    new_height = event.height
    resized_image = background_image.resize((new_width, new_height))
    background_photo = ImageTk.PhotoImage(resized_image)
    background_label.config(image=background_photo)
    background_label.image = background_photo  # 保持对图像的引用，防止被垃圾回收

# 创建主窗口，使用 ttkbootstrap 的样式
root = tb.Window(themename="united")
root.title("月山村春晚抽奖环节")
root.geometry("1600x900")

# 加载自定义背景图片
background_image = Image.open("background_image.png")  # 替换为您的图片路径
background_photo = ImageTk.PhotoImage(background_image)

# 创建一个标签来显示背景图片
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使用place方法放置背景图片标签

# 绑定窗口的<Configure>事件，以便在窗口大小改变时调整图像大小
root.bind("<Configure>", resize_image)
# 自定义样式
style = tb.Style()
style.configure('TButton', font=('Helvetica', 12, 'bold'), foreground='gold')  # 设置按钮字体为金色
style.configure('TLabel', font=('Helvetica',24,'bold'), foreground='#fcbb08', background='red')  # 设置标签字体为白色
style.configure('TFrame', background='red')  # 设置背景颜色为红色


# 标题标签
title_label = tb.Label(root, text="月山村春晚抽奖环节", font=("Helvetica", 40), bootstyle="info", style='TLabel')
title_label.pack(pady=20)
# 创建当前轮次标签
current_round_label = tb.Label(root, text="", font=("Helvetica", 14), bootstyle="light", style='TLabel')
current_round_label.pack(pady=10)


# 创建抽奖按钮
draw_button = tb.Button(root, text="开始抽奖", command=draw_lottery, bootstyle="success-outline", width=20, style='TButton')  # 应用自定义按钮样式
draw_button.pack(pady=30)


# 创建中奖者标签
winner_label = tb.Label(root, text="", font=("Helvetica", 18), bootstyle="light", style='TLabel')
winner_label.pack(pady=20)

# 创建已中奖者标签
winners_label = tb.Label(root, text="", font=("Helvetica", 18), bootstyle="light", style='TLabel')
winners_label.pack(pady=20)

# 创建结果显示标签
result_label = tb.Label(root, text="", font=("Helvetica", 18),
style='TLabel')
result_label.pack(pady=60)

# 版权信息标签
copyright_label = tb.Label(root, text="月山村晚专用", font=(12), bootstyle="secondary", style='TLabel')  # 应用自定义标签样式
copyright_label.pack(side=tk.BOTTOM, pady=20)

# 运行主循环
root.mainloop()