# Staticpressureofliquidcolumn.py
import numpy as np

def cfcpif(well_depth_Z, density_sand, density_fluid, well_diameter, sand_volume_concentration_per_second, displacement_per_second, g):
    # 初始化静压力列表
    pwh_list = []
    # 初始化当前深度为 0
    current_depth = 0

    # 对每秒进行循环以计算静压力（s sand_concentration代表sand_volume_concentration_per_second 中的元素）
    for sand_concentration, displacement in zip(sand_volume_concentration_per_second, displacement_per_second):
        # 根据砂比计算混合流体的密度
        density = sand_concentration * density_sand + (1 - sand_concentration) * density_fluid
        # 计算流速（单位时间内体积通过单位面积的量）
        flow_velocity = 4 * displacement / (np.pi * well_diameter ** 2)
        # 计算每秒液体通过井筒的增加深度（在此简化假设流速恒定）
        additional_depth = flow_velocity
        # 累加当前深度
        current_depth += additional_depth

        # 当前深度超过井深时只计算到井深的部分
        if current_depth > well_depth_Z:
            # 计算当前秒未超出井深部分的静压力并添加到列表
            pwh = density * g * (additional_depth - (current_depth - well_depth_Z))
            pwh_list.append(pwh)
            # 跳出循环，因为已经达到井深
            break
        else:
            # 如果未达到井深，将当前秒的静压力添加到列表
            pwh = density * g * additional_depth
            pwh_list.append(pwh)

    # 如果最终深度小于井深，使用流体密度填充剩余未到井深的静压力
    while len(pwh_list) < len(sand_volume_concentration_per_second):
        pwh_list.append(density_fluid * g * (well_depth_Z - current_depth))
        # 将当前深度更新为井深，虽然在循环中无影响，但有助于理解
        current_depth = well_depth_Z

    # 返回静压力数组，这是计算得到的静压力列表的累积和值
    return np.cumsum(pwh_list)