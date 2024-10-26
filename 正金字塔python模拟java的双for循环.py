def print_pyramid(n):
    for i in range(1, n + 1):
        # 打印前导空格不去換行
        print(' ' * (n - i), end=' ')
        # 打印星号
        print('*' * (2 * i - 1))

# 调用函数，打印高度为5的金字塔
print_pyramid(5)