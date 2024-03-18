# DataProcessing.py
import numpy as np
import matplotlib.pyplot as plt

# 移动平均滤波函数
def smooth_data(data, window_size=5):
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')

# 趋势分析函数
def trend_analysis(X, Y):
    # 移动平均滤波光滑处理
    window_size = 20
    Y_smoothed = smooth_data(Y, window_size)

    # 计算相邻点之间的差分
    dx = np.diff(X)
    dy = np.diff(Y_smoothed)

    # 计算斜率
    slopes = dy / dx
    slopes_smoothed = smooth_data(slopes, window_size)

    # 确定上升段和下降段
    upward_segments = np.where(slopes_smoothed > 0)[0]
    downward_segments = np.where(slopes_smoothed < 0)[0]

    # 绘制原始曲线和光滑曲线
    plt.figure(figsize=(10, 8))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体，确保标签显示汉字
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符
    # 绘制原始曲线
    plt.subplot(2, 1, 1)
    plt.plot(X, Y, 'b-', label='原始曲线')
    plt.plot(X, Y_smoothed, 'r-', label='光滑曲线')
    # 设置横纵坐标范围从0开始
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('曲线平滑处理')

    # 绘制上升段和下降段的标记
    plt.subplot(2, 1, 2)
    plt.plot(X, Y_smoothed, 'b-')

    for i in upward_segments:
        plt.plot([X[i], X[i + 1]], [Y_smoothed[i], Y_smoothed[i + 1]], 'r-')
    for i in downward_segments:
        plt.plot([X[i], X[i + 1]], [Y_smoothed[i], Y_smoothed[i + 1]], 'g-')

    plt.legend(['光滑曲线', '上升段', '下降段'])
    # 设置横纵坐标范围从0开始
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('趋势分析')
    plt.tight_layout()

