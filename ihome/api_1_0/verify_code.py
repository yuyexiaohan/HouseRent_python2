# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome import constants
from flask import current_app, jsonify, make_response, request # ?
from ihome.utils.response_code import RET
from ihome.models import User
import random
from ihome.libs.rlyuntongxun.send_smspy import CCP


# restful风格的url:GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
	"""
	获取图片验证码
	:return: 正常情况：验证码图片 异常：返回json
	"""
	# 业务逻辑处理
	# 生成验证码图片
	name, text, image_data = captcha.generate_captcha()
	# 将验证码图片真实值和编号保存在redis中, 设置有效期
	# redis: string list hash set
	# "key": xxx
	# 使用hash操作，只能整体操作，不符合要求
	# image_codes: {"":"", "":"", "":"",}  hash数据类型 hset("image_codes", "id1", "abc")

	# 单条维护记录
	# 使用set和expire方法进行组合使用，配置存储及过去时间
	# redis_store.set("image_code_%s" % image_code_id, text)
	# # 设置有效期
	# redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)

	# 直接使用setex方法对文本和有效期进行设置
	# redis_store.setex(mage_code_id, 有效期, text)
	try:
		redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
	except Exception as e:
		current_app.logger.error("redis存储图像识别码错误:%s" % e)
		return jsonify(errno=RET.DATAERR, errmsg="save image code id failed")
	# 返回图片
	resp = make_response(image_data)
	resp.headers["Content-Type"] = "image/jpg"
	# print("resp:", resp, type(resp))
	return resp


# url: api/v1.0/sms_codes/<mobile>?image_code=xxxx
@api.route("/sms_codes/<re(r'1[345678]\d{9}'):mobile>")
def get_sms_code(mobile):
	"""获取短信验证码"""
	# 获取参数
	image_code = request.args.get("image_code")
	image_code_id = request.args.get("image_code_id")
	print("image_code：", image_code, "image_coed_id:", image_code_id)

	# 校验参数
	if not all([image_code_id, image_code]):
		# 表示参数不完整
		return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

	# 业务逻辑
	# 从redis中取出真实的图片验证码
	try:
		real_image_code = redis_store.get("image_code_%s" % image_code_id)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="redis数据库异常")
	# 判断图片验证码是否过期
	if real_image_code is None:
		# 表示图片验证码没有或者过期
		return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

	# 比较后，删除图片验证码，需要放在这个位置
	# 删除redis中的图片验证码，在验证1次后，用于防止用户使用同一个验证码进行多次校验
	try:
		redis_store.delete("image_code_%s" % image_code_id)
	except Exception as e:
		current_app.logger.error(e)

	# 与用户填写的值进行对比
	if real_image_code.lower() != image_code.lower():
		# 表示用户验证码填写错误
		return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

	# **********************************************************

	#判断对于这个手机号的操作在60秒内是否有之前的记录，如果有就说明操作频繁，不做处理
	try:
		send_flag = redis_store.get("send_sms_code_%s" % mobile)
	except Exception as e:
		current_app.logger.error(e)
	else:
		if send_flag is not None:
			# 表示60秒内有发送记录
			return jsonify(errno=RET.DATAERR, errmsg="请求过于频繁，请60秒后重新访问！")


	# 判断手机号码是否已经注册
	try:
		user = User.query.filter_by(mobile=mobile).first()
	except Exception as e:
		current_app.logger.error(e)
	else:
		if user:
			return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

	# 如果手机号不存在，则生成短信验证码
	sms_code = "%06d" % random.randint(0, 999999) # 生成6位随机短信验证码
	print("sms_code:", sms_code)

	# 保存真实的短信验证码
	try:
		redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
		# 保存发送给这个手机号的记录，防止用户在60S内重复发送
		redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="短信验证码异常")

	# 发送短信
	try:
		ccp = CCP()
		result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.THIRDERR, errmsg="第三方服务调用异常")

	# 返回值
	if result == 0:
		# 发送成功
		return jsonify(errno=RET.OK, errmsg="发送成功")
	else:
		return jsonify(errno=RET.THIRDERR, errmsg="发送失败")
