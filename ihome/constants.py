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

# 允许登录的错误次数
LOGIN_ERROR_MAX_TIME = 5

# 不允许用户登录的过期时间， 单位：秒
NOT_LOGIN_TIME = 600

# 七牛的域名
QINIU_URL_DOMAIN = "http://pq53vhclw.bkt.clouddn.com/"

# 城区信息的缓存时间, 单位：秒
AREA_INFO_REDIS_CACHE_EXPIRES = 7200

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页数据容量
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面页数缓存时间，单位秒
HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES = 7200