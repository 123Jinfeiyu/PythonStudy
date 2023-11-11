# -*- coding: utf-8 -*-
# @Author : 左手
# @File : aaa.py
# @Software: PyCharm
# @Date : 2023/11/7 20:56
import time
import random
import sys
# # 函数可以返回多个值
# def f(a,b):
#     s = a+b
#     j = a*b
#     return s,j,'hello'
# num1 = f(10,12)
# print(num1)


# 判断字符串是否为数字
# while 1:
#     money = input('请输入金额:')
#     if money.isdigit():
#         print('你输入的是纯数字')
#     else:
#         print('请输入正确金额')

# import time
# now_time = time.strftime('%Y-%m-%d %H:%M:%S')
# print(now_time)
# 初始化局数
d,u,p = 0,0,0
# 出招表
czb = ['石头','剪刀','布']
while 1:  # 死循环
    # 获取当前时间
    local_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f'欢迎来到猜拳游戏！当前的时间是{local_time}')
    pwd = input('请输入密码登录:')
    """
    密码规则：
总共是11位，全部由数字组成，第1位是1，第二位可以是数字3458其中之一，
后面9位任意数字
例如：18601012345、13912367890则满足。 
    """
    if len(pwd) == 11 and pwd.isdigit() and pwd[0] == '1' and pwd[1] in '3458':
        print('欢迎登录，可以进行猜拳了')
        print('==============================')
        # 猜拳
        while 1: # 死循环 2 3 4 5 6 7 8 9
            # 用户的猜拳
            user = input('请进行猜拳(0退出游戏):')
            # 电脑的随机猜拳
            computer = random.choice(czb)
            # 判断用户输入的是不是czb里面的元素
            if user in czb:
                print('出招正确')
                # 用户赢得逻辑
                if (user=='石头') and (computer=='剪刀') or (user=='剪刀') and (computer=='布') or (user=='布') and (computer=='石头'):
                    u += 1
                    print(f'你赢了，电脑出的是{computer}')
                # 平局
                elif user == computer:
                    p += 1
                    print(f'平局，电脑出的是{computer}')
                # 用户输的
                else:
                    d += 1
                    print(f'你输了，电脑出的是{computer}')
            elif user == '0':
                print('你已退出程序')
                print(f'你赢了{u}局，输了{d},平了{p}局')
                sys.exit()
            else:
                print('出错招了')
    else:
        print('你输入的密码有误，请重新输入')





