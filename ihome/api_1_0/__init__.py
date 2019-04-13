# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


# 导入flask的蓝图
from flask import Blueprint



# 创建蓝图对象
api = Blueprint("api_1_0", __name__)

# 导入demo
# 这里注意前后顺序，先初始化api，再导入demo，否则反复调用，demo中的api就不能先查找到
from ihome.api_1_0 import demo