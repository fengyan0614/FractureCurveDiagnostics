import matplotlib.pyplot as plt

def pressure_curve(time, bottomhole_pressure):
    plt.figure(figsize=(10, 8))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体，确保标签显示汉字
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符
    # 创建时间数据，从0到井底净压力数据的长度减1，每个数据点代表1秒
    time_seconds = list(range(len(bottomhole_pressure)))
    # 绘制井底净压力曲线，时间数据设置为从0开始的秒数
    plt.plot(time_seconds, bottomhole_pressure, label="井底净压力曲线")
    plt.xlabel("时间 (秒)")
    plt.ylabel("井底净压力")
    # 设置横纵坐标范围从0开始
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    # 设置图例
    plt.legend()
    # 使用 tight_layout 自动调节布局
    plt.tight_layout()
    # 显示图表
    plt.show()

def plot_combined_curves(time, dataset_tuple, label_tuple, title):
    plt.figure(figsize=(10, 8))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体，确保标签显示汉字
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符
    # 循环遍历每组数据和标签来绘制曲线
    for data, label in zip(dataset_tuple, label_tuple):
        plt.plot(time, data, label=label)

    plt.xlabel('时间 (秒)')
    plt.ylabel('压力 (Pa)')
    plt.title(title)
    plt.grid(True)
    # 设置横纵坐标范围从0开始
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.legend()  # 显示图例
    plt.show()
