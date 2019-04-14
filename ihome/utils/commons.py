# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang


# 导入基础转换器
from werkzeug.routing import BaseConverter


# 定义一个正则转换器
class ReCoverter(BaseConverter):
	"""定义正则表达式转换器"""
	def __init__(self, url_map, regex):
		# 使用super调用父类的处事方法
		super(ReCoverter, self).__init__(url_map)
		# 保存正则表达式
		self.regex = regex