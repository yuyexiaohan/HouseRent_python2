# coding=utf-8 
# Time : 2019/4/19
# Author : achjiang
# Filename : houses

from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, jsonify, request, session
from ihome.utils.response_code import RET
from ihome import db, constants, redis_store
from ihome.models import Area, House, Facility, HouseImage
from ihome.utils.image_storage import storage
import json


# @api.route("/areas", methods="[GET]")
@api.route("/areas")
def get_areas_info():
	"""获取地域信息
	:return json 地域信息
	"""
	# 从redis中获取数据，如果有就显示
	try:
		resp_json = redis_store.get("area_info")
	except Exception as e:
		current_app.logger.error(e)
	else:
		if resp_json is not None:
			# redis有数据
			current_app.logger.info("hit redis area_info")
			return resp_json, 200, {"Content-Type": "application/json"}

	# 如果redis没有数据，查询数据库，获取房屋信息
	# redis数据库缓存数据，后续再网页中调用地域信息
	try:
		area_li = Area.query.all()
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")

	area_dict_li = []
	# 将对象转换为字典
	for area in area_li:
		area_dict_li.append(area.to_dict()) # to_dict是返回一个字典

	# 将数据转换成json字符串
	resp_dict = dict(errno=RET.OK, errmsg="OK", data=area_dict_li)
	resp_json = json.dumps(resp_dict)

	# 将数据保存再redis中
	try:
		redis_store.setex("area_info", constants.AREA_INFO_REDIS_CACHE_EXPIRES, resp_json)
	except Exception as e:
		current_app.logger.error(e)

	return resp_json, 200, {"Content-Type": "application/json"}


@api.route("/houses/info", methods=["POST"])
@login_required
def get_house_info():
	"""获取房屋信息
	前端发送过来的json数据
	{
		"title":"",
		"price":"",
		"area_id":"1",
		"address":"",
		"room_count":"",
		"acreage":"",
		"unit":"",
		"capacity":"",
		"beds":"",
		"deposit":"",
		"min_days":"",
		"max_days":"",
		"facility":["7","8"]
	}
	"""
	# 获取数据
	user_id = g.user_id
	req_houses = request.get_json()

	title = req_houses.get("title")  # 房屋名称标题
	price = req_houses.get("price")  # 房屋单价
	area_id = req_houses.get("area_id")  # 房屋所属城区的编号
	address = req_houses.get("address")  # 房屋地址
	room_count = req_houses.get("room_count")  # 房屋包含的房间数目
	acreage = req_houses.get("acreage")  # 房屋面积
	unit = req_houses.get("unit")  # 房屋布局（几室几厅)
	capacity = req_houses.get("capacity")  # 房屋容纳人数
	beds = req_houses.get("beds")  # 房屋卧床数目
	deposit = req_houses.get("deposit")  # 押金
	min_days = req_houses.get("min_days")  # 最小入住天数
	max_days = req_houses.get("max_days")  # 最大入住天数

	# 校验数据
	if not all([title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
		return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

	# 判断房屋金额是否正确
	try:
		price = int(float(price) * 100)
		deposit = int(float(deposit) * 100)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

	# 判断区域id是否存在
	try:
		area = Area.query.get(area_id)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")
	if area is None:
		return jsonify(errno=RET.NODATA, errmsg="城区信息错误")

	# 保存房屋信息
	house = House(
		user_id=user_id,
		area_id=area_id,
		title=title,
		price=price,
		address=address,
		room_count=room_count,
		acreage=acreage,
		unit=unit,
		capacity=capacity,
		beds=beds,
		deposit=deposit,
		min_days=min_days,
		max_days=max_days
	)

	# db.session.add(house)

	# # 保存数据成功
	# try:
	# 	db.session.add(house)
	# 	db.session.commit()
	# except Exception as e:
	# 	current_app.logger.error(e)
	# 	db.session.rollback()
	# 	return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

	# 处理房屋的设施信息
	facility_ids = req_houses.get("facility")

	# 如果用户勾选了设施信息，在将数据保存到数据库
	if facility_ids:
		try:
			# select  * from ih_facility_info where id in []
			facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
		except Exception as e:
			current_app.logger.error(e)
			return jsonify(errno=RET.DBERR, errmsg="数据库异常")

		if facilities:
			# 表示有合法的设施数据
			# 保存设施数据
			house.facilities = facilities
	# 统一将房屋信息和设施信息提交
	try:
		db.session.add(house)
		db.session.commit()
	except Exception as e:
		current_app.logger.error(e)
		db.session.rollback()
		return jsonify(errno=RET.DBERR, errmsg="脑残数据失败")
		# 保存数据成功
	return jsonify(errno=RET.OK, errmsg="OK", data={"house_id": house.id})


@api.route("/houses/image", methods=["POST"])
@login_required
def save_house_image():
	"""保存房屋图片
	参数 图片 房屋的id
	"""
	image_file = request.files.get("house_image")
	house_id = request.form.get("house_id") # 从form表单中拿去数据

	if not all([image_file, house_id]):
		return jsonify(erron=RET.PARAMERR, errmsg="参数错误")

	# 判断house_id正确性
	try:
		house = House.query.get(house_id)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="数据异常")

	if house is None:
		return jsonify(errno=RET.NODATA, errmsg="数据异常")

	# 读取图片数据
	image_data = image_file.read()
	# 保存图片到七牛云
	try:
		file_name = storage(image_data)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.THIRDERR, errmsg="保存图片失败")

	# 保存图片信息到数据库中
	house_image = HouseImage(
		house_id=house_id,
		url=file_name
	)
	db.session.add(house_image)

	# 处理房屋的主图片
	if not house.index_image_url:
		house.index_image_url = file_name
		db.session.add(house)

	try:
		db.session.commit()
	except Exception as e:
		current_app.logger.error(e)
		db.session.rollback()
		return jsonify(errno=RET.DBERR, errmsg="保存图片信息异常")

	image_url = constants.QINIU_URL_DOMAIN + file_name
	return jsonify(errno=RET.OK, errmsg="图片上传成功", data={"image_url": image_url})






