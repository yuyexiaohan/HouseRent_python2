#!/usr/bin/env python 
# coding=utf-8
# @Time : 2019/4/22 22:32
# @Author : achjiang
# @File : main.py

from celery import Celery
from ihome.tasks import config


# 定义celery对象
celery_app = Celery("ihome")

# 引入配置信息
celery_app.config_from_object(config)

# 自动搜寻异步任务
celery_app.autodiscover_tasks(["ihome.tasks.sms"])