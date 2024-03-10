import matplotlib.pyplot as plt

# 单独绘制井底净压力曲线
def pressure_curve(time, bottomhole_pressure):
    plt.figure(figsize=(12, 9))
    time = time.astype(str)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(time, bottomhole_pressure, label="井底净压力曲线")
    plt.xlabel("时间")
    plt.ylabel("井底净压力")
    max_ticks = 20 # 最多显示20个时间刻度
    tick_spacing = len(time) // max_ticks  # 计算间隔数
    # 选用加粗的其他时间点作为刻度标签
    time_ticks = time[::tick_spacing]  # numpy数组的切片功能，通过指定步长来获取等间隔的时间点
    plt.xticks(range(0, len(time), tick_spacing), time_ticks, rotation=45)    # 设定的间隔过大，导致右上角没有足够的空间来显示完整的 x 轴标签值
    plt.legend()
    plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域

#
# 绘制多坐标轴图，展示井底静压力与其他参数
def multiple_axes_plot(time, bottomhole_pressure, tubing_friction, fluid_column_pressure, perforation_friction):
    fig, ax1 = plt.subplots(figsize=(12, 9))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    color = 'tab:red'
    ax1.set_xlabel('时间')
    ax1.set_ylabel('井筒摩阻', color=color)
    ax1.plot(time, tubing_friction, color=color, label='井筒摩阻')
    ax1.tick_params(axis='y', labelcolor=color)

    # 实例化一个新的轴共享相同的x轴
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('outward', 60))
    color = 'tab:green'
    ax2.set_ylabel('液柱压力', color=color)
    ax2.plot(time, fluid_column_pressure, color=color, label='液柱压力')
    ax2.tick_params(axis='y', labelcolor=color)

    # 再次实例化一个新的轴共享相同的x轴
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 120))
    color = 'tab:purple'
    ax3.set_ylabel('孔眼摩阻', color=color)
    ax3.plot(time, perforation_friction, color=color, label='孔眼摩阻')
    ax3.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
