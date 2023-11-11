# -*- coding: utf-8 -*-
# @Author : 左手
# @File : src.py
# @Software: PyCharm
# @Date : 2023/11/7 20:18
login_user = None
from api import user_interface,bank_interface
from lib import common
from pprint import pprint
def register():
    """注册模块
    a.输入用户名，密码，确认密码(两次输入密码不一致提示输入错误)
    b.输入合法，把得到的数据保存在user_data中
    c.输入不合法就提示异常，合法就进入下一步
    """
    while 1:
        # 1. 要求用户输入用户名和密码
        user_name = input('请输入你的用户名:')
        password = input('请输入你的密码:')
        re_password = input('请确认你的密码:')
        # 2. 判断两次密码一样
        if password == re_password:
            flag,msg = user_interface.register_info(user_name,password)
            if flag:
                print(msg)
                break
            else:
                print(msg)
                break
        else:
            print('两次密码不一致，请重新输入')

def login():
    """登录模块
    1.写个死循环，让程序可以重复执行
    2.让用户输入用户名和密码
    3.进行逻辑判断==》 账号是否存在，密码是否一致 ==》 返回一个结果
    """
    while 1:
        user_name = input('请输入你的用户名:')
        password = input('请输入你的密码:')
        flag,msg = user_interface.login_info(user_name,password)
        if flag:
            print(msg)
            global login_user
            login_user = user_name
            break
        else:
            print(msg)
        # login_info()


@ common.is_login  # cheak_money = is_login(cheak_money)
def cheak_money():
    """查看余额"""
    money = user_interface.cheak_money_info(login_user)  # 只是返回余额(函数)
    print(f'用户{login_user},账号为{money}元')

@ common.is_login
def recharge():
    """存钱模块"""
    while 1:
        money = input('请输入存款金额:')
        if not money.isdigit():
            print('输入错误，请输入正确的金额')
            continue
        else:
            flag,msg = bank_interface.save_money_info(login_user,money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
                break

@ common.is_login
def get_money():
    """取钱模块
    1.让我们用户输入要取款的金额
    2.进行取款的逻辑处理
    3.返回取款结果
    """
    while 1:
        money = input('请输入取金额:')
        if not money.isdigit():
            print('输入错误，请输入正确的金额')
            continue
        else:
            flag,msg = bank_interface.get_money_info(login_user,money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
                break
# 百分之90 都是最后一条报错信息是正确
@ common.is_login
def account():
    """查看账单"""
    acc_list = bank_interface.get_acc(login_user)
    if acc_list:
        pprint(acc_list)
    else:
        print('该用户目前没有流水账单')

# 功能选择的字典
fun_select = {
    0:('退出',exit),
    1:('注册',register),
    2:('登录',login),
    3:('查看余额',cheak_money),
    4:('存钱',recharge),
    5:('取钱',get_money),
    6:('账单',account)
}

def atm():
    print('欢迎来到 左手银行')
    while 1:  #  死循环
        for k in fun_select:  # k = 字典的键
            print(k,fun_select[k][0])  # fun_select[k] = 元祖
        select = int(input('请选择你要做的操作:'))
        if select in fun_select:
            fun_select[select][1]()   #  字典[键] = 值
        else:
            print('输入错误，请重新输入')

atm()

# 数据类型  判断  循环   函数   面向对象


# 1. 基础语法(面向对象)  2. 数据结构与算法  3. 编程题 4. 系统知识