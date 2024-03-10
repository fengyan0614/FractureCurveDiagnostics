# Wellborefriction.py
import numpy as np

# 计算井中的流速,即通过给定直径井筒的流量q
def cffv(q, wdiameter):
    return 4 * q / (np.pi * wdiameter ** 2)

# 根据所提供的流量、流体密度、井筒直径等计算水力摩阻系数
def calculate_hydraulic_friction_coefficient(q, fluid_density, wdiameter, wellbore_roughness, fluid_viscosity):
    Re = fluid_density * cffv(q, wdiameter) * wdiameter / fluid_viscosity
    epsilon = 2 * wellbore_roughness / wdiameter
    if Re <= 0:
        coeff1 = 0.004  # 初始时排量为0，Re=0
    elif Re <= 2000:
        coeff1 = 64 / Re
    elif Re <= (59.7 / epsilon ** (8 / 7)):
        coeff1 = 0.3164 / (Re ** 0.25)
    elif Re < ((665 - 765 * np.log(epsilon)) / epsilon):
        coeff1 = (-1 / (1.8 * np.log(6.9 / Re + (epsilon / 3.7) ** 1.11))) ** 2
    else:
        coeff1 = 1 / (2 * (np.log(3.7 / epsilon) ** 2))

    return float(coeff1) if coeff1 is not None else None

#  通过迭代累加每秒的摩擦压降来计算井筒流动摩阻
def ctfi(displacement_per_second, fluid_density, wdiameter, roughness, fluid_viscosity, well_length, timestep=1):
    # 初始化不同时间每秒的摩阻压降列表
    friction_pressure_drop_per_second = []

    # 初始化当前处理的井段长度
    current_segment_length = 0
    # 初始化摩擦压降积分
    cumulative_friction_pressure_drop = 0

    for q in displacement_per_second:
        # 计算当前流速
        velocity = cffv(q, wdiameter)
        # 计算当前的水力摩阻系数
        hfc = calculate_hydraulic_friction_coefficient(q, fluid_density, wdiameter, roughness, fluid_viscosity)
        # 计算当前流速下单位长度内的摩阻压降
        tubing_friction_pressure_drop_per_length = hfc * fluid_density * velocity ** 2 / (2 * wdiameter)

        # 累加摩擦压降积分，并更新当前处理的井段长度
        cumulative_friction_pressure_drop += tubing_friction_pressure_drop_per_length
        current_segment_length += 1

        # 如果处理的井段长度达到井深，结束循环
        if current_segment_length >= well_length:
            break

        friction_pressure_drop_per_second.append(cumulative_friction_pressure_drop)

# 如果最终处理的井段长度小于井长，使用最后计算的摩阻压降填充剩余部分至输入数据长度一致
    while len(friction_pressure_drop_per_second) < len(displacement_per_second):
        friction_pressure_drop_per_second.append(cumulative_friction_pressure_drop)

    return np.array(friction_pressure_drop_per_second)