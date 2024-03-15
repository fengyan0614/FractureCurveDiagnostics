#  Staticpressureofliquidcolumn.py
import numpy as np

def cfcpif(Q_fluid, Vp_proppant, Proppantmidu, fluidmidu, g, Z, D, detaTime=1):
    deta_Z = []  # 存储各段时间内质点位移增量
    P_well_g = []  # 存储各段时间内的压力

    for k in range(len(Q_fluid)):
        v = 4 * Q_fluid[k] / np.pi / D ** 2  # 计算当前时刻井筒流速
        deta_Z.append(v * detaTime)  # 计算位移增量

        if np.sum(deta_Z) < Z:  # 判断总位移是否小于井深
            well_Z = deta_Z + [Z - np.sum(deta_Z)]  # 记录液柱段长度
            well_Vp = list(Vp_proppant[:k + 1]) + [0]  # 记录液柱段的砂比
        else:
            sum_so_far = 0
            boundary = 0

            # 根据总位移判断液柱段长度和砂比
            for i in range(k, -1, -1):
                sum_so_far += deta_Z[i]
                if sum_so_far > Z:
                    boundary = i
                    break
            well_Z = [deta_Z[i] for i in range(k, boundary, -1)]
            well_Z = well_Z + [Z - np.sum(well_Z)]
            well_Vp = list(Vp_proppant[i] for i in range(k, boundary, -1)) + [Vp_proppant[boundary]]

        # 确保砂比的长度和液柱段的长度一致
        while len(well_Vp) < len(well_Z):
            well_Vp.append(well_Vp[-1])

        # 计算混合液密度
        well_mix_midu = (1 - np.array(well_Vp)) * fluidmidu + np.array(well_Vp) * Proppantmidu
        # 计算压力，存入 P_well_g
        P_well_g.append(np.sum(well_mix_midu * g * np.array(well_Z)))

    return P_well_g  # 返回压力部分
