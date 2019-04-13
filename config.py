# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang

import redis


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

	# flask-session配置：https://pythonhosted.org/Flask-Session/
	# 1.配置flask_session缓存的数据类型，
	# 可以是redis,memcached,mongodb,sqlalchemy,filesystem等
	SESSION_TYPE = "redis"
	# 2.对应redis的配置
	# 本身redis数据库和用于缓存的redis数据库可能是两台不同的服务器，
	# 这里项目为方便使用同一台服务器
	SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
	# 3.配置session数据的有效期
	PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
	"""开发环境配置信息"""
	DEBUG = True
	pass


class ProductionConfig(Config):
	"""生产环境配置信息"""
	pass


# 名字与类的映射
config_map = {
	"develop": DevelopmentConfig,
	"product": ProductionConfig
}