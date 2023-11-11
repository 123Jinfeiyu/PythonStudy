# -*- coding: utf-8 -*-
# @Author : 左手
# @File : user_interface.py
# @Software: PyCharm
# @Date : 2023/11/7 20:17
from db import db_handle
"""
处理用户注册的逻辑
1.用户注册得到的信息(数据)保存起来，方便长期使用
2.把得到的数据交给专门保存数据的模块，把数据保存到本地
"""

# list1 = ['左手','年龄',18,666,175]
# dict1 = {
#     '姓名':'左手',
#     '密码':123456,
#     '存款':2
# }

# 处理注册函数的逻辑
def register_info(user_name,password):
    user_info = {
        'user_name':user_name,
        'password':password,
        'money':1000,   # 注册好了 默认就有1000余额
        'account':[]
    }
    # 查找用户的数据
    user_data = db_handle.select_data(user_name)
    if user_data:
        return False,f'注册失败，该用户名已经存在'
    db_handle.save_data(user_info)
    return True,f'{user_name}注册成功'


"""
处理用户登录的逻辑:
1.先查看用户是否存在==》存在，继续下一步，不存在就显示错误
2.密码是否一致==》一致就登陆成功，不一致就登陆失败
"""
def login_info(user_name,password):
    user_data = db_handle.select_data(user_name)
    if user_data:
        if password == user_data['password']:
            return True,f'{user_name}登陆成功'
        else:
            return False,f'密码错误，请重新输入'
    else:
        return False,'用户不存在，请先注册'

# 查看余额的功能函数实现
# 通过用户名获取用户数据
def cheak_money_info(login_user):
    user_data = db_handle.select_data(login_user)
    return user_data['money']
