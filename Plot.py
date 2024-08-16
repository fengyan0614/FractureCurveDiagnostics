import matplotlib.pyplot as plt

def pressure_curve(time, bottomhole_pressure):
    plt.figure(figsize=(10, 8))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体，确保标签显示汉字
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符
    # 创建时间数据，从0到井底净压力数据的长度减1，每个数据点代表1秒
    time_seconds = list(range(len(bottomhole_pressure)))
    # 将井底净压力数据转换为 MPa 单位
    bottomhole_pressure_mpa = [p / 1000000 for p in bottomhole_pressure]
    # 绘制井底净压力曲线，时间数据设置为从0开始的秒数
    plt.plot(time_seconds, bottomhole_pressure_mpa, label="井底净压力曲线")
    plt.xlabel("时间 (min)")
    plt.ylabel("井底净压力 (MPa)")
    # 设置横纵坐标范围从0开始
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    # 设置图例
    plt.legend()
    # 使用 tight_layout 自动调节布局
    plt.tight_layout()
    # 显示图表
    plt.show()


def plot_combined_curves(time, dataset_tuple, label_tuple, title, new_time, new_pressure):
    fig, ax1 = plt.subplots(figsize=(10, 8))  # 创建一个带有单一y轴的子图
    ax2 = ax1.twinx()  # 创造一个新的y轴，共享同一个x轴
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体，确保标签显示汉字
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示负号

    colors = ['y', 'b', 'g', 'r', 'c', 'm']
    # 循环遍历数据和标签来绘制双y轴曲线
    for i, (data, label) in enumerate(zip(dataset_tuple, label_tuple)):
        if i < 1:  # 前两个数据绘制在第一个y轴
            ax1.plot(time, data, color=colors[i], label=label)
        else:  # 其他的绘制在第二个y轴
            ax2.plot(time, data, color=colors[i], linestyle='--', label=label)
    # 新的数据直接绘制到主Y轴上
    # ax1.plot(new_time+2.3, new_pressure, color='k', label="井底净压力参考值")
    # ax1.plot(new_time , new_pressure, color='k', label="井底净压力参考值")
    ax1.set_xlabel('时间 (min)', fontsize=12)
    ax1.set_ylabel('井筒摩阻 (MPa),井底净压力参考值(MPa),井口压力 (MPa)', fontsize=12)
    ax2.set_ylabel('排量 (m3/min), 砂比(%), 粘度 (mPa·s)', fontsize=12)

    ax1.legend(loc='upper left', fontsize=12)
    ax2.legend(loc='upper right', fontsize=12)

    plt.title(title)
    plt.grid(True)
    ax1.set_ylim(0, 50)  # 设置主y轴的范围
    ax2.set_ylim(0, 60)  # 设置主y轴的范围
    plt.show()
