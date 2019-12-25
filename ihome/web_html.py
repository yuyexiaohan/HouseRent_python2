# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang

# 引入蓝图
from flask import Blueprint, current_app, make_response
# 导入csrf进行跨域保护
from flask_wtf import csrf


# 提供静态文件的蓝图
html = Blueprint("web_html", __name__)

# 127.0.0.1:8080/()
# 127.0.0.1:8080/(index.html)
# 127.0.0.1:8080/register.html
# 127.0.0.1:8080/favicon.ico # 浏览器默认为网络图标，会自己请求这个资源


@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
	"""	提供html文件	"""

	# 如果html_file_name 为空，表示访问路径是'/',访问主页
	if not html_file_name:
		html_file_name = "index.html"
	# 如果资源不是favicon,ico
	if html_file_name != "favicon.ico":
		html_file_name = "html/" + html_file_name

	# 创建一个csrf_token值
	csrf_token = csrf.generate_csrf()

	# flask提供的返回静态文件的全局方法
	response = make_response(current_app.send_static_file(html_file_name))

	# 设置cookie值
	response.set_cookie("csrf_token", csrf_token)

	# 不设置有效期，当前窗口关闭后无效

	return response
