# Wellborefriction.py
import math
import numpy as np
def ctfi(Q_fluid, Vp_proppant, Proppantmidu, fluidmidu, Z, D, R, u,dropoutrate,detaTime=1):
    P_well_f = np.zeros(len(Q_fluid))
    deta_Z = np.zeros(len(Q_fluid))
    lamdas = []  # 用于存储每个时间步的 lamda 值

    for t in range(len(Q_fluid)):
        # 计算当前时间步的流速 v
        v = 4 * Q_fluid[t] / (np.pi * D ** 2)
        # 计算当前时间步的雷诺数 Re
        Re_t = fluidmidu * v * D / u[t]
        # 如果雷诺数不大于零，则跳过当前迭代
        if Re_t < 4000:
            lamda = 64 / Re_t
        else:
            lamda = (1 / (-0.8686 * math.log((R / D) / 3.7 - 1.93 / Re_t * math.log((R / D) / 4.3 ** 1.1 + 6.05 / Re_t))) ** 2)*0.2
        # 将当前时间步的 lamda 值添加到 lamdas 列表
        lamdas.append(lamda)
        # print(lamda)
        # 计算当前时间步的位移增量
        deta_Z[t] = v * detaTime
        # 清除中间信息数据
        well_Z = []  # 更新液柱段
        well_Vp = []  # 更新液柱段的砂比
        well_mix_midu = []  # 更新混合液密度
        # 更新液柱段，液柱段的砂比，和混合液密度
        if np.sum(deta_Z[:t+1]) < Z:
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
        P_well_f[t] = np.sum(np.array(well_Z) * ((lamda / D * v ** 2) * np.array(well_mix_midu) / 2))*dropoutrate
    return P_well_f
