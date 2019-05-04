# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


# 导入flask的蓝图
from flask import Blueprint


# 创建蓝图对象
api = Blueprint("api_1_0", __name__)

# 导入蓝图的视图,建立该蓝图下的视图，运行前都需要导入，否则url无法访问视图函数
# 这里注意前后顺序，先初始化api，再导入demo，否则反复调用，demo中的api就不能先查找到
from . import index, verify_code, passport, profile, houses, orders