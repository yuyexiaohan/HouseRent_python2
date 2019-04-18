# coding=utf-8 
# Time : 2019/4/17
# Author : achjiang
# Filename : passport

from . import api
# 获取前端参数, jsonfy(创建一个json)
from flask import request, jsonify, current_app, session
from ihome.utils.response_code import RET
import re
# 导入redis实例对象
from ihome import redis_store, db, constants
from ihome.models import User
from sqlalchemy.exc import IntegrityError


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
	password2 = req_dict.get("password2")

	# 校验参数
	if not all([mobile, sms_code, password]):
		return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

	# 检验手机号
	if not re.match(r"1[34578]\d{9}", mobile):
		# 表示格式不对
		return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

	# 验证密码,简单只是验证密码是否一致，复杂的可以密码格
	# 式长度等
	if password != password2:
		# 密码错误
		return jsonify(errno=RET.PARAMERR, errmsg="两次输入密码不一致")

	# 从redis中取出短信验证码
	try:
		real_sms_code = redis_store.get("sms_code_%s" % mobile)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DATAERR, errmsg="验证码错误")

	# 验证短信验证码是否过期
	if real_sms_code is None:
		return jsonify(errno=RET.NODATA, errmsg="短信验证码已失效")

	# 删除redis中存储的短信验证码，防止被重复使用
	try:
		redis_store.delete("sms_code_%s" % mobile)
	except Exception as e:
		current_app.logger.error(e)

	# 判断用户短信验证码是否正确
	if real_sms_code != sms_code:
		return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

	# 判断用户的手机号是否注册过
	# try:
	#     user = User.query.filter_by(mobile=mobile).first()
	# except Exception as e:
	#     current_app.logger.error(e)
	#     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
	# else:
	#     if user is not None:
	#         # 表示手机号已存在
	#         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

	# 保存用户注册信息和判断用户是否注册可以同时操作
	# 密码加密放在User模型类里进行操作
	user = User(name=mobile, mobile=mobile)
	user.password = password  # 设置属性

	try:
		db.session.add(user)
		db.session.commit()
	except IntegrityError as e:
		# 数据库操作错误后的回滚
		db.session.rollback()
		# 表示手机号出现了重复值，即手机号已注册过
		current_app.logger.error(e)
		return jsonify (errno=RET.DATAEXIST, errmsg="手机号已存在")
	except Exception as e:
		# 数据库操作错误后的回滚
		db.session.rollback()
		# 表示手机号出现了重复值，即手机号已注册过
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

	# 保存登录状态到session中
	session["name"] = mobile
	session["mobile"] = mobile
	session["user_id"] = user.id

	# 返回结果
	return jsonify (errno=RET.OK, errmsg="注册成功")

@api.route("/sessions", methods=["POST"])
def login():
	"""用户登录"""
	req_dic = request.get_json()
	mobile = req_dic.get("mobile")
	password = req_dic.get("password")

	# 数据完整性判断
	if not all([mobile, password]):
		return jsonify(errno=RET.DATAERR, errmsg="参数错误")

	# 手机号格式
	if not re.match(r"1[34578]\d{9}", mobile):
		return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

	# 判断错误次数，限制，超过则返回
	# redis记录："access_nums_请求的ip":"次数"
	user_ip = request.remote_addr  # 获取用户IP
	try:
		access_nums = redis_store.get("access_num_%s" % user_ip)
	except Exception as e:
		current_app.logger.error(e)
	else:
		if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIME:
			return jsonify(errno=RET.REQERR, errmsg="登录错误次数过多，请稍后再试！")

	# 使用手机号查询用户
	try:
		user = User.query.filter_by(mobile=mobile).first()
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DATAERR, errmsg="获取用户数据失败！")

	# 判断数据是否匹配
	if user is None or not user.check_password(password):
		# 如果失败，记录失败次数，返回信息
		try:
			redis_store.incr("access_num_%s" % user_ip)
			redis_store.expire("access_num_%s" % user_ip, constants.NOT_LOGIN_TIME)
		except Exception as e:
			current_app.logger.error(e)
		return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

	# 如果验证成功，将登录状态保存在session的缓存中
	session["name"] = user.name
	session["mobile"] = user.mobile
	session["user_id"] = user.id
	return jsonify(errno=RET.OK, errmsg="登录成功")

@api.route("/session", methods=["GET"])
def check_login():
	"""检查登陆状态"""
	# 尝试从session中获取用户的名字
	name = session.get("name")
	# 如果session中数据name名字存在，则表示用户已登录，否则未登录
	if name is not None:
		return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
	else:
		return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
	"""登出"""
	# 清除session数据
	session.clear()
	return jsonify(errno=RET.OK, errmsg="OK")