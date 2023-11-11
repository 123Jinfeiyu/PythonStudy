# -*- coding: utf-8 -*-
# @Author : 左手
# @File : db_handle.py
# @Software: PyCharm
# @Date : 2023/11/7 20:18
import json
from config.setting import user_data
import os
# 作用: 专门对数据进行保存以及读取，修改的模块
def save_data(user_info):
    user_name = user_info['user_name'] # 把用户名取出来等下给文件命名
    with open(f'{user_data}/{user_name}.json','w',encoding='utf-8') as f:
        # dump 将python对象转成json格式存入文件
        # dumps 将python对象转成json格式的字符串
        json.dump(user_info,f)


# mvc 开发模式  ==》 架构分明  ==》 更好的开发以及管理

# m ==》 model ==》模块层  ==》 增删改查 数据更新

# v ==》 view ==》 视图层 ==》 用户看到的东西

# c ==> controller  ==> 控制层 ==》用户交互  控制行为的

# 查找用户的数据
def select_data(user_name):
    user_path = f'{user_data}/{user_name}.json'
    # os模块  判断文件是否存在
    if os.path.exists(user_path):  # True
        with open(user_path,'r',encoding='utf-8')as f:
            # load 是对文件进行操作的，load的主要参数是打开的文件
            # loads 是对字符串进行操作的，loads的主要参数是字符串
            yhsj = json.load(f)
            return yhsj