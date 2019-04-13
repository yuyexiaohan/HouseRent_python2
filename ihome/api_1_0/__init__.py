# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


# 导入flask的蓝图
from flask import Blueprint
# 导入demo
from . import demo


# 创建蓝图对象
api = Blueprint("api_1_0", __name__)
