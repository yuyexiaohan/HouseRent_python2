# coding=utf-8 
# Time : 2019/4/19
# Author : achjiang
# Filename : houses

from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, jsonify, request, session
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome import db, constants
from ihome.models import Area


# @api.route("/areas", methods="[GET]")
@api.route("/areas")
# @login_required
def get_areas_info():
	"""获取地域信息"""
	# 查询数据库，获取房屋信息
	print("*" * 20)
	try:
		area_li = Area.query.all()
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")

	area_dict_li = []
	# 将对象转换为字典
	for area in area_li:
		area_dict_li.append(area.to_dict()) # to_dict是返回一个字典
	return jsonify(errno=RET.OK, errmsg="OK", data=area_dict_li)



