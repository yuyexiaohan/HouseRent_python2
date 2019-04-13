# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


from flask import Flask


app = Flask(__name__)

#
@app.route("/v1.0/index")
def index():
	return "index page"