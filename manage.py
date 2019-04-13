# coding=utf-8 
# Time : 2019/1/7
# Author : achjiang


# 导入flask框架
from flask import Flask
# 导入SQLAlchemy用以创建数据库
from flask_sqlalchemy import SQLAlchemy
import redis
# 导入session
from flask_session import Session


# I 创建app
app = Flask(__name__)


class Config(object):
	"""配置信息"""
	DEBUG = True

	SECRET_KEY = "SDA008*LLQW"

	# mysql数据库配置：
	# 1.设置连接数据库的URL
	SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome_python2"
	# 2.设置每次请求结束后会自动提交数据库中的改动
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	# redis
	REDIS_HOST = "127.0.0.1"
	REDIS_PORT = 6379

	# flask-session配置
	SESSION_TYPE = "redis"
	# 本身redis数据库和用于缓存的redis数据库可能是两台不同的服务器，这里项目为方便使用同一台服务器
	SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)





# II 将配置信息导入到app当中
app.config.from_object(Config)

# III 创建数据库
db = SQLAlchemy(app)

# IV redis缓存-session
redis_store = redis.SrtictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 利用flask_session 将session数据保存到redis数据库中
Session(app)

#
@app.route("/index")
def index():
	return "index page"


if __name__ == "__main__":
	app.run()