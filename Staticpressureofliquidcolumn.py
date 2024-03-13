#  Staticpressureofliquidcolumn.py
import numpy as np


def cfcpif(displacement_per_second, sand_concentration, density_sandu, density_fluid, g, well_depth_Z, well_diameter,
           time_step=1):
    pwh_list = []  # 静压力列表
    well_Z = []  # 井筒段长度列表
    well_mix_midu = []  # 混合液密度列表

    for k, displacement in enumerate(displacement_per_second):
        # 新增液柱段长度
        new_segment_length = displacement * time_step / (np.pi * (well_diameter / 2) ** 2)

        # 计算混合密度
        new_segment_density = ((1 - sand_concentration[k]) * density_fluid +
                               sand_concentration[k] * density_sandu)

        # 如果新段加上现有液柱长度不会超过井深，则直接添加
        if sum(well_Z) + new_segment_length <= well_depth_Z:
            well_Z.append(new_segment_length)
            well_mix_midu.append(new_segment_density)
        else:
            # 如果累积长度超过了井深，需要调整最顶端液柱段的长度
            excess_length = (sum(well_Z) + new_segment_length) - well_depth_Z
            # 找到足够删除的长度
            while excess_length > 0 and well_Z:
                if well_Z[0] > excess_length:
                    well_Z[0] -= excess_length
                    excess_length = 0
                else:
                    excess_length -= well_Z.pop(0)
                    well_mix_midu.pop(0)
            # 添加新的液柱段到列表
            well_Z.append(new_segment_length)
            well_mix_midu.append(new_segment_density)

        # 确保well_Z和well_mix_midu的长度一致
        assert len(well_Z) == len(well_mix_midu), "well_Z和well_mix_midu的长度必须一致"

        # 计算当前时间步的静压力
        P_well_g = np.sum(np.multiply(well_Z, well_mix_midu)) * g
        pwh_list.append(P_well_g)

    return pwh_list
