# main.py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# from bottomholePressure import cpf, cfcpif, calculate_bottomhole_pressure, pressure_curve, ctfi
from Staticpressureofliquidcolumn import cfcpif
from Wellborefriction import ctfi
from Orificefriction import cpf
from NetpressureBottom import calculate_bottomhole_pressure
from Plot import pressure_curve, multiple_axes_plot
import datetime
import matplotlib.dates as mdates

# 读取 Excel 数据
def read_excel_data(excel_path):
    df = pd.read_excel(excel_path)
    return df

# 读取Excel文件的路径
file_path = r"C:\Users\fy\Desktop\4-15\焦页4HF\焦页4HF压裂数据\焦页4HF井第1段压裂施工\压裂\2013-12-15焦页4HF井第一段压裂施工数据（秒点）.SVD.xlsx"
g = 9.8  # 重力加速度，单位 m/s²
# 读取Excel文件中排量和砂浓度的数据
data = pd.read_excel(file_path, header=11)
time = data['时间(hh:mm:ss)']
displacement = data['排量(m^3/Min)'].values  # Excel文件中的排量列
displacement_per_second = displacement / 60  # 立方米每分钟化为立方米每秒
sand_ratio = data['砂比(%)'].values  # Excel文件中的砂浓度列
sand_concentration = sand_ratio/100  # 百分比化为小数
wellhead_pressure_MPa = data['油压(MPa)'].values  # Excel文件中的排量列
wellhead_pressure = wellhead_pressure_MPa*1000000
time_as_float = mdates.date2num([datetime.datetime.combine(datetime.date.today(), t) for t in time])
# 其它参数定义
well_depth_Z = 2636  # 井深，单位为米
well_length_L = 4006  # 井筒长度，单位为米
density_sand = 1780  # 砂的密度，单位 kg/m³
density_fluid = 1004.5  # 流体的密度，单位 kg/m³
well_diameter = 0.3397  # 井筒直径，单位 m
min_horizontal_stress = 48600000  # 最小水平主应力，单位 Pa
pdiameter = 0.0095 # 孔眼直径 m
perforation_flow_coefficient = 0.95 #孔眼流量系数
fluid_viscosity = 0.012  # 读取压裂液黏度，Pa·s
wellbore_roughness = 0.0001  # 读取井筒管壁绝对粗糙度，m
perforation_quantity = 60

# 计算井底静压力并绘制曲线
def calculate_bottomhole_pressure_from_excel(excel_path):
    # 初始化孔眼摩阻数组
    perforation_friction = np.zeros_like(displacement_per_second)

    # 井筒内携沙液柱静压力
    fluid_integral = cfcpif(well_depth_Z, density_sand, density_fluid, well_diameter, sand_concentration, displacement_per_second, g)
    # 井筒流动摩阻
    tubing_friction_integral = ctfi(displacement_per_second, density_fluid, well_diameter, wellbore_roughness, fluid_viscosity, well_length_L)
    # 计算井底净压力
    bottomholepressure = calculate_bottomhole_pressure(wellhead_pressure,  fluid_integral, tubing_friction_integral, perforation_friction, min_horizontal_stress)
    # 得到结果列表，将其保存到文件
    # 遍历排量数组计算孔眼摩阻
    for i, displacement in enumerate(displacement_per_second):
        perforation_friction[i] = cpf(displacement, density_fluid, perforation_quantity, pdiameter, perforation_flow_coefficient)

    # 创建一个pandas DataFrame
    df = pd.DataFrame({
        'Time': time,
        'fluid_integral': fluid_integral,
        'tubing_friction_integral': tubing_friction_integral,
        'perforation_friction': perforation_friction,
        'Pressure': bottomholepressure
    })
    file_path = r"C:\Users\fy\Desktop\4-15\4-15\焦页4HF\焦页4HF压裂数据\焦页4HF井第1段压裂施工\压裂\bottomholepressure.xlsx.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')

    # 绘制井底压力曲线
    pressure_curve(time, bottomholepressure)
    # 绘制多坐标曲线
    multiple_axes_plot(time_as_float, bottomholepressure, tubing_friction_integral, fluid_integral, perforation_friction)
    plt.show()
    # 返回所需的所有变量
    return time, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction


if __name__ == "__main__":

    excel_path = r"C:\Users\fy\Desktop\4-15\焦页4HF\焦页4HF压裂数据\焦页4HF井第1段压裂施工\压裂\2013-12-15焦页4HF井第一段压裂施工数据（秒点）.SVD.xlsx"
    try:
        time, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction = calculate_bottomhole_pressure_from_excel(
            excel_path)
        pressure_curve(time, bottomholepressure)
        multiple_axes_plot(time_as_float, bottomholepressure, tubing_friction_integral, fluid_integral,
                           perforation_friction)
    except Exception as e:
        print(f"An error occurred: {e}")
