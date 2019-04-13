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


# I 创建app
app = Flask(__name__)








# II 将配置信息导入到app当中
app.config.from_object(Config)

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