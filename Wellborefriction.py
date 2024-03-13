# Wellborefriction.py
import numpy as np

def cffv(q, wdiameter):
    return 4 * q / (np.pi * wdiameter ** 2)

def calculate_hydraulic_friction_coefficient(q, mixed_density, wdiameter, wellbore_roughness, fluid_viscosity):
    v = cffv(q, wdiameter)
    epsilon = 2 * wellbore_roughness / wdiameter
    Re = mixed_density * v * wdiameter / fluid_viscosity

    small_number = np.finfo(float).eps
    Re_safe = np.maximum(Re, small_number)
    epsilon_safe = np.maximum(epsilon, small_number)

    lamda = np.where(Re_safe <= 2000, 64 / Re_safe, 0)
    lamda = np.where((Re_safe > 2000) & (Re_safe <= (59.7 / epsilon_safe**(8/7))), 0.3164 / Re_safe**(0.25), lamda)
    lamda = np.where((Re_safe > (59.7 / epsilon_safe**(8/7))) & (Re_safe < (665 - 765 * np.log(epsilon_safe)) / epsilon_safe),
                    (1 / (-1.8 * np.log(6.9 / Re_safe + (epsilon_safe / 3.7)**1.11)))**2, lamda)
    lamda = np.where(Re_safe >= ((665 - 765 * np.log(epsilon_safe)) / epsilon_safe),
                    1 / (2 * (np.log(3.7 / epsilon_safe))**2), lamda)

    return lamda

def ctfi(displacement_per_second, sand_concentration, density_sand, density_fluid, well_diameter, well_length_L, wellbore_roughness, fluid_viscosity, time_step=1):
    # 初始化数组
    fluid_integral = np.zeros(len(displacement_per_second))

    for i in range(len(displacement_per_second)):
        # 计算流速
        flow_velocity = cffv(displacement_per_second[i], well_diameter)

        # 计算水力摩阻系数
        hfc = calculate_hydraulic_friction_coefficient(displacement_per_second[i], density_fluid, well_diameter,
                                                       wellbore_roughness, fluid_viscosity)

        # 计算混合液密度
        mixed_density = (1 - sand_concentration[i]) * density_fluid + sand_concentration[i] * density_sand

        # 计算单段压降
        unit_pressure_drop = (hfc / well_diameter) * (flow_velocity ** 2) * (mixed_density / 2)

        # 计算总压降
        total_pressure_drop = unit_pressure_drop * well_length_L

        # 存储结果
        fluid_integral[i] = total_pressure_drop

    return fluid_integral
