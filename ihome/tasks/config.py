#!/usr/bin/env python 
# coding=utf-8
# @Time : 2019/4/22 22:32
# @Author : achjiang
# @File : config.py

BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'