import sympy as sp

# 定义一个3x3有理数矩阵
matrix = sp.Matrix([[1, 0, 2],
                   [2, 1, 4],
                   [3, -2, 7]])

# 计算逆矩阵
inverse_matrix = matrix.inv()

# 使用sp.simplify来简化分数
inverse_matrix_simplified = sp.simplify(inverse_matrix)

# 打印逆矩阵
print("原矩阵:")
print(matrix)
print("逆矩阵:")
print(inverse_matrix_simplified)

import numpy as np
# 原始矩阵
A = np.array([[1, 0, 2],
              [2, 1, 4],
              [3, -2, 7]])
# 候选逆矩阵
B = np.array([[15, -4, -2],
              [-2, 1, 0],
              [-7, 2, 1]])
# 计算矩阵乘积
result = np.dot(A, B)
# 定义单位矩阵
identity_matrix = np.identity(3)
# 检查结果是否接近单位矩阵
is_inverse = np.allclose(result, identity_matrix)

if is_inverse:
    print("B 是 A 的逆矩阵")
else:
    print("B 不是 A 的逆矩阵")
