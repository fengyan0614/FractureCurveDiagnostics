# Orificefriction.py
# 计算孔眼摩阻
def cpf(displacement, density_fluid, quantity, pdiameter, coeff2):
    # 该函数现在接受单个流量值，并返回计算得到的单个摩擦值
    friction = 8.1 * density_fluid * (displacement ** 2) / ((coeff2 ** 2 )* (quantity ** 2 )* (pdiameter ** 4))
    return friction