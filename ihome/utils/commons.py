# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang

# 导入基础转换器
from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from ihome.utils.response_code import RET
import functools


# 定义一个正则转换器
class ReCoverter(BaseConverter):
	"""定义正则表达式转换器"""
	def __init__(self, url_map, regex):
		# 使用super调用父类的处事方法
		super(ReCoverter, self).__init__(url_map)
		# 保存正则表达式
		self.regex = regex


# 登录检测装饰器
def login_required(view_func):

	@functools.wraps(view_func) # 保障文件名不变的一个装饰器
	def wrapper(*args, **kwargs):
		# 判断用户的登录状态
		user_id = session.get("user_id")

		# 如果用户时登录状态，就执行视图
		if user_id is not None:
			# 将user_id保存在g对象中，在视图函数中可以通过g对象获取保存数据
			g.user_id = user_id
			return view_func(*args, **kwargs)
		else:
			# 如果未登录，返回未登录的信息
			return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
	return wrapper
