#!/usr/bin/env python 
# coding=utf-8
# @Time : 2019/4/22 0:06
# @Author : achjiang
# @File : task_sms.py

from celery import Celery
from ihome.libs.rlyuntongxun.send_smspy import CCP


# 定义celery对象
celery_app = Celery("ihome", broker="redis://127.0.0.1:6379/1")


@celery_app.task
def send_sms(to, datas, temp_id):
    """
    发送短信异步任务
    :param to:
    :param datas:
    :param temp_id:
    :return:
    """
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)

    # celery开启的命令
    # celery -A ihome.tasks.task_sms worker -l info