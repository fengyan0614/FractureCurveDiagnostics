# main.py
import numpy as np
import pandas as pd
from Staticpressureofliquidcolumn import cfcpif
from Wellborefriction import ctfi
from Orificefriction import cpf
from NetpressureBottom import calculate_bottomhole_pressure
from Plot import pressure_curve, plot_combined_curves
import traceback
from Dataprocessing import analyze_and_plot_extension_modes

# 读取 Excel 数据
def read_excel_data(excel_path):
    df = pd.read_excel(excel_path)
    return df
# 读取Excel文件的路径
file_path = r"C:\Users\fy\Desktop\2-5HF数据整理\焦页2-5HF排量砂比整理\2-5HF-5.xlsx"
g = 9.8  # 重力加速度，单位 m/s²
# 读取Excel文件中排量和砂浓度的数据
data = pd.read_excel(file_path, header=0)
displacement = data['排量'].values  # Excel文件中的排量列
displacement_per_second = displacement / 60  # 立方米每分钟化为立方米每秒
sand_ratio = data['砂比'].values  # Excel文件中的砂浓度列
sand_concentration = sand_ratio/100  # 百分比化为小数
wellhead_pressure_MPa = data['施工泵压'].values  # Excel文件中的排量列
wellhead_pressure = wellhead_pressure_MPa*1000000
time_in_seconds = data['时间s']
# 确保数据框的粘度列是数值类型
data['液体粘度'] = pd.to_numeric(data['液体粘度'], errors='coerce')
fluid_viscosity = data['液体粘度'] / 1000
well_depth_Z = 2863  # 井深，单位为米
well_length_L = 4960  # 井筒长度，单位为米
density_sand = 1510  # 支撑剂密度，单位 kg/m³
density_fluid = 1000  # 压裂液密度，单位 kg/m³
well_diameter = 0.115  # 井筒直径，单位 m
# min_horizontal_stress = 50000000  # 23-Z2HF-26最小水平主应力，单位 Pa
min_horizontal_stress = 75000000# 149-1HF-24最小水平主应力，单位 Pa
pdiameter = 0.0122  # 孔眼直径 m
perforation_flow_coefficient = 0.95  # 孔眼流量系数
# fluid_viscosity = 0.012  # 压裂液黏度，Pa·s  #黏度为定值
wellbore_roughness = 0.00001  # 井筒管壁绝对粗糙度，m
perforation_quantity = 42  # 孔眼数量，个
dropoutrate = 0.8


# 计算井底净压力并绘制曲线
def calculate_bottomhole_pressure_from_excel(excel_path):
    displacement = data['排量'].values  # Excel文件中的排量列
    displacement_per_second = displacement / 60  # 立方米每分钟化为立方米每秒
    sand_ratio = data['砂比'].values  # Excel文件中的砂浓度列
    sand_concentration = sand_ratio / 100  # 百分比化为小数
    viscosity = data['液体粘度']
    fluid_viscosity = viscosity / 1000

    # 井筒内携沙液柱静压力
    fluid_integral = cfcpif(displacement_per_second,  sand_concentration, density_sand, density_fluid, g, well_depth_Z, well_diameter)
    # 井筒流动摩阻
    tubing_friction_integral = ctfi(displacement_per_second, sand_concentration, density_sand, density_fluid,  well_length_L, well_diameter, wellbore_roughness, fluid_viscosity, 1-dropoutrate)
    # 计算孔眼摩阻
    perforation_friction = cpf(displacement_per_second, density_fluid, density_sand, sand_concentration, perforation_quantity, pdiameter,perforation_flow_coefficient)
    # 计算井底净压力
    bottomholepressure = calculate_bottomhole_pressure(wellhead_pressure,  fluid_integral, tubing_friction_integral, perforation_friction, min_horizontal_stress)


    # # 定义要绘制的数据集和标签
    tfi = [val / 1000000 for val in tubing_friction_integral]
    fi = [val / 1000000 for val in fluid_integral]
    pf = [val / 1000000 for val in perforation_friction]
    wp = [val / 1000000 for val in wellhead_pressure]
    wp1 = [val-20 for val in wp]
    bp = [val / 1000000 for val in bottomholepressure]
    tis = [val / 60 for val in time_in_seconds]

    # # 将排量、砂比和粘度添加到数据集和标签中
    # dataset_tuple = (wp1, displacement, sand_ratio, viscosity)
    # label_tuple = ('井口压力预测值(MPa)', '排量(m3/s)', '砂比', '粘度(Pa.s)')
    # # 绘制多坐标曲线
    # plot_combined_curves(tis, dataset_tuple, label_tuple, '压力参数随时间变化图')
    # dataset_tuple1 = (tfi, fi, pf, wp, bp)
    # label_tuple1 = ('井筒摩阻 (MPa)', '液柱压力 (MPa)', '孔眼摩阻 (MPa)', '井口压力(MPa)', '井底净压力(MPa)')
    # dataset_tuple2 = (tfi, wp, displacement, sand_ratio, viscosity)
    # label_tuple2 = ('井筒摩阻 (MPa)', '井口压力(MPa)', '排量 (m3/min) ', '砂比(%)', '粘度 (mPa·s)')
    # dataset_tuple3 = (fi, wp, displacement, sand_concentration, fluid_viscosity)
    # label_tuple3 = ('液柱压力 (MPa)', '井口压力(MPa)', '排量 (m3/s) ', '砂比', '粘度 (Pa·s)')
    dataset_tuple4 = (bp, displacement, sand_ratio, viscosity)
    label_tuple4 = ('井底净压力(MPa)', '排量 (m3/min) ', '砂比（%', '粘度 (mPa·s)')
    # dataset_tuple5 = (bp,  wp, displacement, sand_ratio, viscosity)
    # label_tuple5 = ('井底净压力(MPa)', '井口压力(MPa)', '排量 (m3/min) ', '砂比（%）', '粘度 (mPa·s)')
    # 绘制多坐标曲线
    plot_combined_curves(tis, dataset_tuple4, label_tuple4, '149-1HF-24段压裂', tis,  bottomholepressure)
    # 绘制井底压力曲线
    pressure_curve(time_in_seconds, bottomholepressure)
    analyze_and_plot_extension_modes(time_in_seconds, bottomholepressure)

    return time_in_seconds, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction

# 保存数据到Excel文件
def save_to_excel(bottomholepressure, output_path):
    # 确保净压力值为正并转换单位
    bp = [abs(val) / 1000000 for val in bottomholepressure]

    # 创建新的数据框
    new_data = pd.DataFrame({
        'Pressureb': bp
    })

    # 保存新的数据到Excel文件
    new_data.to_excel(output_path, index=False)

if __name__ == "__main__":
    excel_path = r"C:\Users\fy\Desktop\2-5HF数据整理\焦页2-5HF排量砂比整理\2-5HF-5.xlsx"
    output_path = r"C:\Users\fy\Desktop\test.xlsx"
    try:
        # 调用函数并接收返回值
        time_in_seconds, bottomholepressure, fluid_integral, tubing_friction_integral, perforation_friction = calculate_bottomhole_pressure_from_excel(excel_path)
        # 保存数据到Excel文件
        save_to_excel(bottomholepressure, output_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()




