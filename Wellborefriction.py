# Wellborefriction.py

import numpy as np
def ctfi(Q_fluid, Vp_proppant, Proppantmidu, fluidmidu, Z, D, R, u, detaTime=1):
    P_well_f = np.zeros(len(Q_fluid))
    lamdas = []
    deta_Z = np.zeros(len(Q_fluid))

    for t in range(len(Q_fluid)):
        # 根据雷诺数计算水力摩阻系数
        v = 4 * Q_fluid[t] / (np.pi * D ** 2)  # 当前时刻井筒流速
        epsilon = 2 * R / D  # 井筒壁面粗糙程度
        Re = fluidmidu * v * D / u  # 流动雷诺数

        if Re < 2000:
            lamda = 64 / Re  # 计算水力摩阻系数
        elif 2000 < Re < 59.7 / epsilon ** (8 / 7):
            lamda = 0.3164 / Re ** (0.25)
        elif 59.7 / epsilon ** (8 / 7) < Re < (665 - 765 * np.log(epsilon)) / epsilon:
            lamda = (1 / (-1.8 * np.log(6.8 / Re + (R / (3.7 * D)) ** 3.11))) ** 2
        elif Re > (665 - 765 * np.log(epsilon)) / epsilon:
            lamda = 1 / (2 * np.log(3.7 * D / R)) ** 2

        lamdas.append(lamda)  # 计算的lamda值添加到lamdas数组中
        deta_Z[t] = v * detaTime

        # 清除中间信息数据
        well_Z = []  # 更新液柱段
        well_Vp = []  # 更新液柱段的砂比
        well_mix_midu = []  # 更新混合液密度

        # 更新液柱段，液柱段的砂比，和混合液密度
        if np.sum(deta_Z[:t+1])<Z:
            well_Z = list(deta_Z[:t+1]) + [Z - np.sum(deta_Z[:t+1])]
            well_Vp = list(Vp_proppant[:t+1]) + [0]
        else:
            sum_so_far = 0
            boundary = 0
            for i in range(t, -1, -1):
                sum_so_far += deta_Z[i]
                if sum_so_far > Z:
                    boundary = i
                    break
            well_Z = list(deta_Z[i] for i in range(t, boundary, -1)) + [Z - np.sum(deta_Z[i] for i in range(t, boundary, -1))]
            well_Vp = list(Vp_proppant[i] for i in range(t, boundary, -1)) + [Vp_proppant[boundary]]

        well_mix_midu = [(1 - well_Vp[i]) * fluidmidu + well_Vp[i] * Proppantmidu for i in range(len(well_Z))]
        P_well_f[t] = np.sum(np.array(well_Z) * ((lamda / D * v ** 2) * np.array(well_mix_midu) / 2))  # 井筒摩阻

    return P_well_f
