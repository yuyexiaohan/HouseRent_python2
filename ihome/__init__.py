# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


# 导入flask框架
from flask import Flask
# 从config.py文件中导入配置信息
from config import config_map
# 导入SQLAlchemy用以创建数据库
from flask_sqlalchemy import SQLAlchemy
# 导入redis用于缓存
import redis
# 导入session
from flask_session import Session
# 前端的csrf防护机制
from flask_wtf import CSRFProtect




# 创建数据库
# 创建数据库需要flask的app对象，所以这里不能直接使用：
# db = SQLAlchemy(app)
# flask框架可以先初始化一个app，然后再在app被创建后执行
# 将db.init_app(app)放入工厂模式中，当app被创建时，就执行
db = SQLAlchemy()

# redis缓存-session
redis_store = None

# I 工厂模式用于创建不同的app实例，例如开发环境app/测试环境app
# 创建app并将配置信息导入到app中
def create_app(config_name):
	"""
	创建flask的应用对象9
	:param config_name: str 配置模式的模式名字（"develop", "product"）
	:return: object 返回创建的app
	"""
	# 创建app
	app = Flask (__name__)

	# 根据对象名获取配置参数的类
	config_class = config_map.get(config_name)
	# 将配置信息导入到app当中
	app.config.from_object (config_class)

	# 使用app初始化db
	db.init_app(app) # flask自带功能

	# 初始化redis工具
	global redis_store
	redis_store = redis.StrictRedis (host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

	# 利用flask_session 将session数据保存到redis数据库中
	Session (app)  # 把Session当作类，将app作为参数传入这个类中

	# 为flask补充csrf防护机制
	CSRFProtect (app)  # 把CSRFProtect当作类，将app作为参数传入这个类中
	# 导入创建的蓝图
	from ihome import api_1_0
	# 注册蓝图
	app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

	# 返回创建的app
	return app

