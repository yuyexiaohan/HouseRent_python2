# coding=utf-8 
# Time : 2019/4/19
# Author : achjiang
# Filename : houses

from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, jsonify, request, session
from ihome.utils.response_code import RET
from ihome import db, constants, redis_store
from ihome.models import Area, House, Facility, HouseImage, User,Order
from ihome.utils.image_storage import storage
import json
import datetime


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


@api.route("/user/houses/", methods=["GET"])
@login_required
def get_user_houses():
	"""获取房东房源信息"""
	user_id = g.user_id

	try:
		user = User.query.get(user_id)
		houses = user.houses
	except Exception as e:
		current_app.logger.error(e)
		return jsonify (errno=RET.DBERR, errmsg="获取参数失败")

# 将查询的房屋信息转换成字典放在列表中
	houses_list = []
	if houses:
		for house in houses:
			houses_list.append(house.to_basic_dict())
	return jsonify(errno=RET.OK, errmsg="ok", data={"houses": houses_list})


@api.route("/houses/index", methods=["GET"])
def get_house_index():
	"""获取主页幻灯片展示的房屋基本信息"""
	# 从缓存中尝试获取数据
	try:
		ret = redis_store.get("home_page_data")
	except Exception as e:
		current_app.logger.error(e)
		ret = None

	if ret:
		current_app.logger.info("hit house index info redis")
		# 因为redis中保存的是json字符串，所以直接进行字符串拼接返回
		return '{"errno":0, "errmsg":"OK", "data":%s}' % ret, 200, {"Content-Type": "application/json"}
	else:
		try:
			# 查询数据库，返回房屋订单数目最多的5条数据
			houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
		except Exception as e:
			current_app.logger.error(e)
			return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

		if not houses:
			return jsonify(errno=RET.NODATA, errmsg="查询无数据")

		houses_list = []
		for house in houses:
			# 如果房屋未设置主图片，则跳过
			if not house.index_image_url:
				continue
			houses_list.append(house.to_basic_dict())

		# 将数据转换为json，并保存到redis缓存
		json_houses = json.dumps(houses_list)  # "[{},{},{}]"
		try:
			redis_store.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRES, json_houses)
		except Exception as e:
			current_app.logger.error(e)

		return '{"errno":0, "errmsg":"OK", "data":%s}' % json_houses, 200, {"Content-Type": "application/json"}


@api.route("/houses/<int:house_id>", methods=["GET"])
def get_house_detail(house_id):
	"""获取房屋详情"""
	# 前端在房屋详情页面展示时，如果浏览页面的用户不是该房屋的房东，则展示预定按钮，否则不展示，
	# 所以需要后端返回登录用户的user_id
	# 尝试获取用户登录的信息，若登录，则返回给前端登录用户的user_id，否则返回user_id=-1
	user_id = session.get("user_id", "-1")

	# 校验参数
	if not house_id:
		return jsonify(errno=RET.PARAMERR, errmsg="参数确实")

	# 先从redis缓存中获取信息
	try:
		ret = redis_store.get("house_info_%s" % house_id)
	except Exception as e:
		current_app.logger.error(e)
		ret = None
	if ret:
		current_app.logger.info("hit house info redis")
		return '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, ret), \
			   200, {"Content-Type": "application/json"}

	# 查询数据库
	try:
		house = House.query.get(house_id)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

	if not house:
		return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

	# 将房屋对象数据转换为字典
	try:
		house_data = house.to_full_dict()
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DATAERR, errmsg="数据出错")

	# 存入到redis中
	json_house = json.dumps(house_data)
	try:
		redis_store.setex("house_info_%s" % house_id, constants.HOUSE_DETAIL_REDIS_EXPIRE_SECOND, json_house)
	except Exception as e:
		current_app.logger.error(e)

	resp = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, json_house), \
		   200, {"Content-Type": "application/json"}
	return resp


# GET /api/v1.0/houses?sd=2017-12-01&ed=2017-12-31&aid=10&sk=new&p=1
@api.route("/houses")
def get_house_list():
	"""获取房屋的列表信息（搜索页面）"""
	start_date = request.args.get("sd", "")  # 用户想要的起始时间
	end_date = request.args.get("ed", "")  # 用户想要的结束时间
	area_id = request.args.get("aid", "")  # 区域编号
	sort_key = request.args.get("sk", "new")  # 排序关键字
	page = request.args.get("p")  # 页数

	# 处理时间
	try:
		if start_date:
			start_date = datetime.strptime(start_date, "%Y-%m-%d")

		if end_date:
			end_date = datetime.strptime(end_date, "%Y-%m-%d")

		if start_date and end_date:
			assert start_date <= end_date
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.PARAMERR, errmsg="日期参数有误")

	# 判断区域id
	if area_id:
		try:
			area = Area.query.get(area_id)
		except Exception as e:
			current_app.logger.error(e)
			return jsonify(errno=RET.PARAMERR, errmsg="区域参数有误")

	# 处理页数
	try:
		page = int(page)
	except Exception as e:
		current_app.logger.error(e)
		page = 1

	# 获取缓存数据
	redis_key = "house_%s_%s_%s_%s" % (start_date, end_date, area_id, sort_key)
	try:
		resp_json = redis_store.hget(redis_key, page)
	except Exception as e:
		current_app.logger.error(e)
	else:
		if resp_json:
			return resp_json, 200, {"Content-Type": "application/json"}

	# 过滤条件的参数列表容器
	filter_params = []

	# 填充过滤参数
	# 时间条件
	conflict_orders = None

	try:
		if start_date and end_date:
			# 查询冲突的订单
			conflict_orders = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date).all()
		elif start_date:
			conflict_orders = Order.query.filter(Order.end_date >= start_date).all()
		elif end_date:
			conflict_orders = Order.query.filter(Order.begin_date <= end_date).all()
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")

	if conflict_orders:
		# 从订单中获取冲突的房屋id
		conflict_house_ids = [order.house_id for order in conflict_orders]

		# 如果冲突的房屋id不为空，向查询参数中添加条件
		if conflict_house_ids:
			filter_params.append(House.id.notin_(conflict_house_ids))

	# 区域条件
	if area_id:
		filter_params.append(House.area_id == area_id)

	# 查询数据库
	# 补充排序条件
	if sort_key == "booking":  # 入住做多
		house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
	elif sort_key == "price-inc":
		house_query = House.query.filter(*filter_params).order_by(House.price.asc())
	elif sort_key == "price-des":
		house_query = House.query.filter(*filter_params).order_by(House.price.desc())
	else:  # 新旧
		house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())

	# 处理分页
	try:
		#                               当前页数          每页数据量                              自动的错误输出
		page_obj = house_query.paginate(page=page, per_page=constants.HOUSE_LIST_PAGE_CAPACITY, error_out=False)
	except Exception as e:
		current_app.logger.error(e)
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")

	# 获取页面数据
	house_li = page_obj.items
	houses = []
	for house in house_li:
		houses.append(house.to_basic_dict())

	# 获取总页数
	total_page = page_obj.pages

	resp_dict = dict(errno=RET.OK, errmsg="OK", data={"total_page": total_page, "houses": houses, "current_page": page})
	resp_json = json.dumps(resp_dict)

	if page <= total_page:
		# 设置缓存数据
		redis_key = "house_%s_%s_%s_%s" % (start_date, end_date, area_id, sort_key)
		# 哈希类型
		try:
			# redis_store.hset(redis_key, page, resp_json)
			# redis_store.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)

			# 创建redis管道对象，可以一次执行多个语句
			pipeline = redis_store.pipeline()

			# 开启多个语句的记录
			pipeline.multi()

			pipeline.hset(redis_key, page, resp_json)
			pipeline.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)

			# 执行语句
			pipeline.execute()
		except Exception as e:
			current_app.logger.error(e)

	return resp_json, 200, {"Content-Type": "application/json"}




