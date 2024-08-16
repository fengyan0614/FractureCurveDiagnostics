import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

def analyze_and_plot_extension_modes(X, P_net, interval=60):
    # 弹出对话框要求输入起始点和结束点
    ROOT = tk.Tk()
    ROOT.withdraw()  # 用户不需要看到一个空的 Tkinter 窗口出现
    start_input = simpledialog.askstring(title="设置起始点", prompt="请输入起始点位置（单位：秒）:")
    end_input = simpledialog.askstring(title="设置结束点", prompt="请输入结束点位置（单位：秒）:")
    ROOT.destroy()  # 销毁Tkinter主窗口

    # 将输入的值（字符串）转换为整数
    try:
        start_point = int(start_input)
        end_point = int(end_input)
    except ValueError:
        raise ValueError("请输入一个有效的整数作为起始点和结束点位置。")

    # 确保 X 和 P_net 是 NumPy 数组
    X = np.array(X)
    P_net = np.array(P_net)

    # 确定起始点和结束点的索引
    start_idx = start_point // interval  # 使用用户输入确定起始索引
    end_idx = end_point // interval  # 使用用户输入确定结束索引
    if start_idx * interval >= len(X) or end_idx * interval > len(X):
        raise ValueError("起始点或结束点位置超出数据范围。")
    if start_idx >= end_idx:
        raise ValueError("起始点应小于结束点。")

    # 从指定的起始点和结束点索引之间取数据
    X = X[start_idx * interval:end_idx * interval]  # 从用户指定的点开始取数据
    P_net = P_net[start_idx * interval:end_idx * interval]  # 从用户指定的点开始取数据

    # 简化重采样逻辑，每隔 interval（这里是 60 秒）取一个数据点
    indices = np.arange(0, len(X), interval)
    X_60_points = X[indices]
    P_net_60_points = P_net[indices]

    # 计算对数差分
    epsilon = 1e-10  # 小的正数，以避免取零或负数的对数
    X_60_points_log = np.log(X_60_points + epsilon)
    P_net_60_points_log = np.log(P_net_60_points + epsilon)
    dx = np.diff(X_60_points_log)
    dy = np.diff(P_net_60_points_log)

    # 计算斜率
    n = dy / dx

    # 平滑处理斜率
    window_size = 1  # 窗口大小，MATLAB 中使用的是 [window_size/2, window_size/2]，这里简化为 1
    n_smoothed = np.convolve(n, np.ones(window_size) / window_size, mode='valid')

    # 限制斜率的绝对值
    n_smoothed = np.clip(n_smoothed, -20, 20)

    # 归一化斜率
    n_smoothed = n_smoothed / 10

    # 分类延伸模式
    Y_n = np.zeros_like(n_smoothed, dtype=int)  # 使用 int 类型以存储分类编号
    for i, value in enumerate(n_smoothed):
        if value > 0.5 or (value > -0.5 and value < -0.3):
            Y_n[i] = 4  # 缝网扩展
        elif 0 < value and value <= 0.5:
            Y_n[i] = 3  # 缝高受限
        elif -0.3 < value and value < 0:
            Y_n[i] = 2  # 缝高扩展
        elif value <= -0.5:
            Y_n[i] = 1  # 突破屏障
        else:
            Y_n[i] = 0  # 其他

    valid_classifications = np.isin(Y_n, [1, 2, 3, 4])

    # 绘图
    plt.figure(figsize=(10, 8))

    # 第一个子图：裂缝延伸模式指数
    plt.subplot(2, 1, 1)  # 2行1列的第一个
    plt.plot(X_60_points[:-1] / 60, n_smoothed, 'b', linewidth=1)
    plt.xlim([0, 200])
    plt.ylim([-4, 4])
    plt.xticks(fontsize=14)
    plt.yticks([-4, -3, -2, -1, 0, 1, 2, 3, 4], fontsize=14)
    plt.ylabel('裂缝延伸模式指数', fontsize=14)
    plt.grid(True)
    plt.title('裂缝延伸模式指数')

    # 第二个子图：延伸模式分类
    plt.subplot(2, 1, 2)  # 2行1列的第二个
    plt.plot(X_60_points[:-1][valid_classifications] / 60, Y_n[valid_classifications], 'r+', markersize=5)
    # 绘制每种模式的代表点，并添加图例
    counts = {1: np.sum(Y_n == 1), 2: np.sum(Y_n == 2), 3: np.sum(Y_n == 3), 4: np.sum(Y_n == 4)}
    mode_labels = ['突破屏障', '缝高扩展', '缝高受限', '缝网扩展']
    for i in [1, 2, 3, 4]:
        plt.plot([], [], ' ', markersize=0, label=f'{mode_labels[i - 1]}{counts[i]} min')

    plt.xlim([0, 200])
    plt.xticks(fontsize=14)
    plt.ylim([-0.5, 4.5])
    plt.yticks([1, 2, 3, 4], fontsize=14)
    plt.gca().invert_yaxis()  # 翻转 y 轴
    plt.gca().set_yticklabels(['突破屏障', '缝高扩展', '缝高受限', '缝网扩展'])
    plt.xlabel('施工时间，min', fontsize=14)
    plt.ylabel('延伸模式', fontsize=14)
    plt.grid(True)
    plt.title('延伸模式分类')
    plt.legend(loc='upper right', handlelength=0)  # 可以调整图例的位置
    plt.tight_layout()  # 调整子图布局以防止标签重叠
    plt.show()
