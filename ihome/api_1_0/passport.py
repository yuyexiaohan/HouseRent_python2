# coding=utf-8 
# Time : 2019/4/17
# Author : achjiang
# Filename : passport

from . import api
# 获取前端参数, jsonfy(创建一个json)
from flask import request, jsonify


@api.route("/users", methods=["POST"])
def register():
	"""注册
	请求参数：手机号、短信验证码、密码
	参数格式：json
	"""
	# 接收前端参数， 获取json数据返回字典
	req_dict = request.get_json()
	mobile = req_dict.get("mobile")
	sms_code = req_dict.get("sms_code")
	password = req_dict.get("password")

	# 校验参数
	if not all([mobile, sms_code, password]):
		return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
