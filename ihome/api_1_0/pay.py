#!/usr/bin/env python 
# coding=utf-8
# @Time : 2019/5/6
# @Author : achjiang
# @File : pay.py


from . import api
from ihome.utils.commons import login_required
from ihome.models import Order
from flask import g, current_app, jsonify, request
from ihome.utils.response_code import RET
from alipay import AliPay
from ihome import constants, db
import os


@api.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    """发起支付宝支付"""
    user_id = g.user_id

    # 判断订单状态
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id, Order.status == "WAIT_PAYMENT").first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if order is None:
        return jsonify(errno=RET.NODATA, errmsg="订单数据有误")

    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016092100559424",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),  # 私钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order.id,  # 订单编号
        total_amount=str(order.amount/100.0),   # 总金额
        subject=u"爱家租房 %s" % order.id,  # 订单标题
        return_url="http://127.0.0.1:5000/payComplete.html",  # 返回的连接地址
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 构建让用户跳转的支付连接地址
    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    print("pay-url:", pay_url)
    return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})


@api.route("/order/payment", methods=["PUT"])
def save_order_payment_result():
    """保存订单支付结果"""
    alipay_dict = request.form.to_dict()
    # 'alipay_dict:',
    # {
    # 'trade_no': u'2019050622001476141000057947',
    # 'seller_id': u'2088102176558614',
    # 'total_amount': u'600.00',
    # 'timestamp': u'2019-05-06 22:19:48',
    # 'charset': u'utf-8',
    # 'app_id': u'2016092100559424',
    # 'sign': u'hQGBJAlD1s7tBpJDcDzRyYve8yjtaCXgSX53uSAkmv7bpT8ecOJnhz9FQZZ5wutfPpXqxUMUm4rodyOFEGZynya6r1UCb88E5g6Rg1YN7NFTQpDt97VyJK273Ep43e4IjfMKl++P4ADp9zWTSCgMcGioKMchUzL+JgkRdrFHpgjBG+J45ZxmQvGXRMSpYQf+7PdgzwN/k+1RMVTOOpol8b7rOgBLp+hN9x6zIBGQL0YXdmfJlxt/NnY/u4b8nQhi4JI7jA05Ux3b/4pRdks0S/uUarzXi0jFiG7rpK193QuSyUVyX+3bb0eVwjIJ46npbehYtVQhPfq03k6I0NZkOQ==',
    # 'out_trade_no': u'6',
    # 'version': u'1.0',
    # 'sign_type': u'RSA2',
    # 'auth_app_id': u'2016092100559424',
    # 'method': u'alipay.trade.wap.pay.return'
    # }

    # 对支付宝的数据进行分离  提取出支付宝的签名参数sign 和剩下的其他数据
    alipay_sign = alipay_dict.pop("sign")

    # 创建支付宝sdk的工具对象
    alipay_client = AliPay(
        appid="2016092100559424",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),  # 私钥
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 借助工具验证参数的合法性
    # 如果确定参数是支付宝的，返回True，否则返回false
    result = alipay_client.verify(alipay_dict, alipay_sign)

    if result:
        # 修改数据库的订单状态信息
        order_id = alipay_dict.get("out_trade_no")
        trade_no = alipay_dict.get("trade_no")  # 支付宝的交易号
        try:
            Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()

    return jsonify(errno=RET.OK, errmsg="OK")
