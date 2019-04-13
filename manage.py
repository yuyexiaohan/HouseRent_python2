# coding=utf-8 
# Time : 2019/1/7
# Author : achjiang


# 导入flask框架
from flask import Flask
# 导入SQLAlchemy用以创建数据库
from flask_sqlalchemy import SQLAlchemy
# 导入redis用于缓存
import redis
# 导入session
from flask_session import Session
# 前端的csrf防护机制
from flask_wtf import CSRFProtect
# 从config.py文件中导入配置信息
from config import config_map


# I 工厂模式用于创建不同的app实例，例如开发环境app/测试环境app
# 创建app并将配置信息导入到app中
def create_app(config_name):
	"""
	创建flask的应用对象
	:param config_name: str 配置模式的模式名字（"develop", "product"）
	:return: object 返回创建的app
	"""
	# 1.创建app
	app = Flask (__name__)

	# 2.根据对象名获取配置参数的类
	config_class = config_map.get(config_name)
	# 3.将配置信息导入到app当中
	app.config.from_object (config_class)
	# 4.返回创建的app
	return app

# II 创建app实例
app = create_app("develop")

# III 创建数据库
db = SQLAlchemy(app)

# IV redis缓存-session
redis_store = redis.SrtictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 利用flask_session 将session数据保存到redis数据库中
Session(app)    # 把Session当作类，将app作为参数传入这个类中

# V 为flask补充csrf防护机制
CSRFProtect(app)    # 把CSRFProtect当作类，将app作为参数传入这个类中


#
@app.route("/index")
def index():
	return "index page"


if __name__ == "__main__":
	app.run()