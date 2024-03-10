# NetpressureBottom.py
# 计算井底净压力
def calculate_bottomhole_pressure(wellhead_pressure, fluid_integral, tubing_friction_integral, perforation_friction, min_horizontal_stress):
    bottomhole_pressure = wellhead_pressure + fluid_integral - tubing_friction_integral - perforation_friction - min_horizontal_stress
    # print("wellhead_pressure:", wellhead_pressure)
    # print("fluid_integral:", fluid_integral)
    # print("tubing_friction_integral:", tubing_friction_integral)
    # print("perforation_friction:", perforation_friction)
    # print("min_horizontal_stress:", min_horizontal_stress)
    # print("bottomhole_pressure:", bottomhole_pressure)
    return bottomhole_pressure