# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang


from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome import constants
from flask import current_app, jsonify, make_response # ?
from ihome.utils.response_code import RET


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
	return resp


