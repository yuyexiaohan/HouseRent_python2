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


@api.route("/areas", methods="[GET]")
@login_required
def get_areas_info():
	"""获取地域信息"""
	# 查询数据库，获取房屋信息
	
	#
	pass



