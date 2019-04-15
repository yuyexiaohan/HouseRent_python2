# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang


from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store


# restful风格的url:GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>
@api.route("/get_image_code")
def get_image_code(image_code_id):
	"""
	获取图片验证码
	:return: 验证码图片
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
	redis_store.set("image_code_%s" % image_code_id, text)
	# 设置有效期
	redis_store.expire("image_code_%s" % image_code_id, 180)

	# 返回图片


