# Orificefriction.py
import numpy as np

# 计算孔眼摩阻
def cpf(displacement_per_second, fluid_density, sand_density, sand_concentration, quantity, pdiameter, coeff2):
    # 初始化摩阻数组
    friction_array = np.zeros(len(displacement_per_second))

    # 遍历displacement_per_second数组的每个元素
    for i, displacement in enumerate(displacement_per_second):
        mixed_density = (1 - sand_concentration[i]) * fluid_density + sand_concentration[i] * sand_density
        friction_array[i] = 0.81 * mixed_density * (displacement ** 2) / ((coeff2 ** 2) * (quantity ** 2) * (pdiameter ** 4))

    return friction_array
