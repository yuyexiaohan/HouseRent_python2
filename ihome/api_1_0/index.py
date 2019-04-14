# coding=utf-8 
# Time : 2019/4/14
# Author : achjiang


from . import api
from ihome import db, models
from flask import current_app
import logging

#
@api.route("/index")
def index():
	# logging.error('error')
	# logging.warning('warning')
	# logging.info('info')
	# logging.debug('debug')
	current_app.logger.error('error msg')
	current_app.logger.warn('warn msg')
	current_app.logger.info('info msg')
	current_app.logger.debug('debug msg')
	return "index page"