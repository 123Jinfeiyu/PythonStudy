# -*- coding: utf-8 -*-
# @Author : 左手
# @File : bank_interface.py
# @Software: PyCharm
# @Date : 2023/11/7 20:18
from db import db_handle
import time
"""
取款函数
"""
def get_money_info(login_user,money):
    """
    1.获取用户数据==》查看现有余额
    2.判断账户里面有没有那么多钱
    3.修改余额/提示取款异常，存款不足
    4.保存数据==》修改余额，添加流水账单
    5.返回取款结果和取款说明明细
    :return: 1.取款结果 2.取款的说明明细
    """
    # 1.通过用户名 获取用户信息
    user_data = db_handle.select_data(login_user)
    # 2.查看余额
    user_money = int(user_data['money'])
    # 3. 判断余额是否足够
    money = int(money)
    if user_money >= money:
        # 4.修改余额的数据
        user_money -= money
        user_data['money'] = user_money
        # 5.添加流水账单信息
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # 返回取款的信息
        acc_info = f'{now_time}   用户{login_user},取款{money}元成功'
        user_data['account'].append(acc_info)
        # 6.保存数据
        db_handle.save_data(user_data)
        return True,acc_info
    return False,'您的账户余额不足，请重新输入'


"""
存钱逻辑
"""
def save_money_info(login_user,money):
    """
    1.获取用户数据==》查看现有余额
    2.修改余额
    3.保存数据==》修改余额，添加流水账单
    4.返回存款结果和存款说明明细
    """
    # 1.通过用户名 获取用户信息
    user_data = db_handle.select_data(login_user)
    # 2.修改余额
    user_data['money'] += int(money)
    # 3.添加流水账单
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    # 返回取款的信息
    acc_info = f'{now_time}   用户{login_user},存款{money}元成功'
    user_data['account'].append(acc_info)
    # 4.保存数据
    db_handle.save_data(user_data)
    return True,acc_info

"""查看账单"""
def get_acc(login_user):
    user_data = db_handle.select_data(login_user)
    return user_data['account']