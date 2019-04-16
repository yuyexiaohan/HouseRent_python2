# coding=utf-8 
# Time : 2019/4/15
# Author : achjiang

# 常量文件汇总

# 图像验证码在redis中的有效期， 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 180


# 短信验证码在redis中的有效期， 单位：秒
SMS_CODE_REDIS_EXPIRES = 300

# 发送短信验证码的间隔 单位：秒
SEND_SMS_CODE_INTERVAL = 60