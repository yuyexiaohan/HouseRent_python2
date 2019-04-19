# coding=utf-8 
# Time : 2019/4/18
# Author : achjiang
# Filename : image_storage

# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file


#需要填写你的 Access Key 和 Secret Key
# access_key = self_config.Access_Key
access_key = "AnE70UQaiqokVXUT7v3BGYNAVWo5oey8UA3fEdsD"
# secret_key = self_config.Secret_Key
secret_key = "BIGPCz55HcnTtq3RqDgMfeLUtvwTaBGnVKNs4gyN"


def storage(file_data):
	"""
	上传文件到七牛
	:param file_data: 上传的文件
	:return:
	"""
	#构建鉴权对象
	q = Auth(access_key, secret_key)

	#要上传的空间
	# bucket_name = self_config.Bucket_Name
	bucket_name = "python2"

	# #上传后保存的文件名
	# key = 'my-python-logo.png'

	#生成上传 Token，可以指定过期时间等
	token = q.upload_token(bucket_name, None, 3600)

	# #要上传文件的本地路径
	# localfile = './sync/bbb.jpg'

	ret, info = put_file(token, None, file_data)
	print(info)
	print("*"*20)
	print(ret)
	# assert ret['key'] == key
	# assert ret['hash'] == etag(localfile)

	if info.status_code == 200:
		# 表示上传成功, 返回文件名
		return ret.get ("key")
	else:
		# 上传失败
		raise Exception ("上传七牛失败")

if __name__ == '__main__':
	file_path = str("./1.jpg")
	with open(file_path, "rb") as f:
		file_data = f.read()
		storage(file_data)
