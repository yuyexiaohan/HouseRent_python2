#coding=utf-8

from CCPRestSDK import REST

# 主帐号
accountSid= "8aaf070864b08c210164cf273a6811d8"


# 主帐号Token
accountToken= 'e162517fca694a4a931d79cbfa6b74c5'

# 应用Id
appId='8aaf070864b08c210164cf273ac411df'

# 请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

# 请求端口
serverPort='8883'

# REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id


class CCP(object):
    """自己封装的发送短信的辅助类"""
    # def __init__(self):
    instance = None

    def __new__(cls):
        # 单例模式
        # 判断CCP类有没有已经剑豪的对象，如果没有，创建一个对象，并保存
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)

            # 初始化REST SDK
            obj.rest = REST (serverIP, serverPort, softVersion)
            obj.rest.setAccount (accountSid, accountToken)
            obj.rest.setAppId (appId)

            cls.instance = obj
        return cls.instance

        # 如果有，则将保存的对象直接返回




    def send_template_sms(self, to, datas, temp_id):
        """

        :param to:
        :param datas:
        :param temp_id:
        :return:
        """
        result = self.rest.sendTemplateSMS (to, datas, temp_id)
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems ():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送成功
            return 0
        else:
            # 发送失败
            return -1


# def sendTemplateSMS(to,datas,tempId):
#     """"""
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)

if __name__ == '__main__':
    ccp = CCP()
    # print("---------")
    ccp.send_template_sms("13163253909", ["1234", "5"], 1)
    # print("*********")

    #sendTemplateSMS(手机号码,内容数据,模板Id)