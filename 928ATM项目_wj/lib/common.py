# -*- coding: utf-8 -*-
# @Author : 左手
# @File : common.py
# @Software: PyCharm
# @Date : 2023/11/7 20:18

from core import src
"""
    常用的功能模块，自定义的功能模块
"""
def is_login(func):
    def cheak(*args,**kwargs):
        # 先判断登录状态
        if src.login_user:  # 代表我已经登陆成功
            # func相当于cheak_money 函数
            # res 相当于 money 钱
            res = func(*args,**kwargs)  # print('你是登录状态')\
            return res
        else:
            print('请登录')
            src.login()

    return cheak
