# main.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Staticpressureofliquidcolumn import cfcpif
from Wellborefriction import ctfi
from Orificefriction import cpf
from NetpressureBottom import calculate_bottomhole_pressure
from Plot import pressure_curve, plot_combined_curves
from datetime import time
import traceback
from Dataprocessing import trend_analysis


# 读取 Excel 数据
def read_excel_data(excel_path):
    df = pd.read_excel(excel_path)
    return df
# 读取Excel文件的路径
file_path = r"C:\Users\fy\Desktop\4-15\4-15\焦页4HF\焦页4HF压裂数据\焦页4HF井第1段压裂施工\压裂\Pump data.xlsx"
g = 9.8  # 重力加速度，单位 m/s²
# 读取Excel文件中排量和砂浓度的数据
data = pd.read_excel(file_path, header=0)

displacement = data['排量'].values  # Excel文件中的排量列
displacement_per_second = displacement / 60  # 立方米每分钟化为立方米每秒
sand_ratio = data['砂比'].values  # Excel文件中的砂浓度列
sand_concentration = sand_ratio/100  # 百分比化为小数
wellhead_pressure_MPa = data['井口压力'].values  # Excel文件中的排量列
wellhead_pressure = wellhead_pressure_MPa*1000000
time_in_seconds = data['时间s']
# 其它参数定义
well_depth_Z = 2636  # 井深，单位为米
well_length_L = 4006  # 井筒长度，单位为米
density_sand = 2500  # 砂的密度，单位 kg/m³
density_fluid = 1004.5  # 流体的密度，单位 kg/m³
well_diameter = 0.14  # 井筒直径，单位 m
min_horizontal_stress = 48600000  # 最小水平主应力，单位 Pa
pdiameter = 0.0095  # 孔眼直径 m
perforation_flow_coefficient = 0.95  # 孔眼流量系数
fluid_viscosity = 0.012  # 压裂液黏度，Pa·s
wellbore_roughness = 0.0001  # 井筒管壁绝对粗糙度，m
perforation_quantity = 60  # 孔眼数量，个



# 计算井底静压力并绘制曲线
def calculate_bottomhole_pressure_from_excel(excel_path):
    # 井筒内携沙液柱静压力
    fluid_integral = cfcpif(displacement_per_second,  sand_concentration, density_sand, density_fluid, g, well_depth_Z, well_diameter)
    # 井筒流动摩阻
    tubing_friction_integral = ctfi(displacement_per_second, sand_concentration, density_sand,density_fluid,  well_length_L, well_diameter, wellbore_roughness, fluid_viscosity)
    # 计算孔眼摩阻
    perforation_friction = cpf(displacement_per_second, density_fluid, density_sand, sand_concentration, perforation_quantity, pdiameter,perforation_flow_coefficient)
    # 计算井底净压力
    bottomholepressure = calculate_bottomhole_pressure(wellhead_pressure,  fluid_integral, tubing_friction_integral, perforation_friction, min_horizontal_stress)

    # 数据处理：将井底净压力的负值设为0
    bottomholepressure[bottomholepressure < 0] = 0

    # 平滑处理：对井底净压力进行移动平均滤波光滑处理
    # 趋势分析：识别曲线的上升段和下降段，并在图形中进行标记
    trend_analysis(time_in_seconds, bottomholepressure)
    # 得到结果列表，将其保存到文件

    # 创建一个pandas DataFrame
    df = pd.DataFrame({
        'Time': np.array(time_in_seconds),
        'fluid_integral': np.array(fluid_integral),
        'tubing_friction_integral': np.array(tubing_friction_integral),
        'perforation_friction': np.array(perforation_friction),
        'Pressure': np.array(bottomholepressure)
    })
    file_path = r"C:\Users\fy\Desktop\4-15\4-15\焦页4HF\焦页4HF压裂数据\焦页4HF井第1段压裂施工\压裂\bottomholepressure.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    # 多坐标曲线的数据及数据标签
    dataset_tuple = (tubing_friction_integral, fluid_integral, perforation_friction, wellhead_pressure, bottomholepressure)
    label_tuple = ('井筒摩阻 (Pa)', '液柱压力 (Pa)', '孔眼摩阻 (Pa)', '井口压力(Pa)', '井底净压力(Pa)')
    # # 绘制多坐标曲线
    plot_combined_curves(time_in_seconds, dataset_tuple, label_tuple, '压力参数随时间变化图')
    # 返回所需的所有变量
    return time, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction


if __name__ == "__main__":

    excel_path = r"C:\Users\fy\Desktop\4-15\4-15\焦页4HF\焦页4HF压裂数据\焦页4HF井第1段压裂施工\压裂\Pump data.xlsx"
    try:
        time_in_seconds, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction = calculate_bottomhole_pressure_from_excel(excel_path)
        pressure_curve(time_in_seconds, bottomholepressure)

    except Exception as e:
        print(f"An error occurred: {e}")

        traceback.print_exc()  # 这将打印错误的堆栈跟踪信息
