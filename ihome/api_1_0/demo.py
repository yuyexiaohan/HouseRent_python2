# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


from . import api
from ihome import db
from flask import current_app

#
@api.route("/index")
def index():
	return "index page"