# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.basic import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

import meizu_weather, youdao_fy, tuling

WECHAT_TOKEN = "yeliangtoken870206"
AppID = "wx2611ba5d5e60a7f9"
AppSecret = ""

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=None
    )

@csrf_exempt
def index(request):
    if request.method == 'GET':
        # 检验合法性.
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml).
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # 解析本次请求的 XML 数据.
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息.
    message = wechat_instance.get_message()

    # 关注事件以及不匹配时的默认回复.
    response = wechat_instance.response_text(
        content=(
            "感谢您的关注！"
            "\n输入【天气xx】来查看xx天气的信息！ 例如输入：天气福州"
            "\n输入【翻译xx】将英文翻译成中文，也可以将中文翻译成英文！ 例如输入：翻译你好；或者输入：翻译hello"
            "\n输入【帮助】查看更多的支持的功能"
            ))

    if isinstance(message, TextMessage):
        # 当前的会话内容.
        content = message.content.strip()
        print content[:1]
        if content == "帮助":
            reply_text = (
                "\n输入【天气xx】来查看xx天气的信息！ 例如输入：天气福州"
                "\n输入【翻译xx】将英文翻译成中文，也可以将中文翻译成英文！ 例如输入：翻译你好；或者输入：翻译hello"
                # "\n输入【快递】可以查询您的快递信息！ 例如输入：快递顺丰1234567890"
                "\n输入【帮助】查看更多的支持的功能"
                "\n【<a href='http://119.29.143.106/getmovielist/'>我的电影收藏</a>】"
            )
            response = wechat_instance.response_text(content=reply_text)
        elif content[:1] == u"天气":
            city_name = content[2:]
            reply_text = meizu_weather.get_weather_data(city_name)
            response = wechat_instance.response_text(content=reply_text)
        elif content[:1] == u"翻译":
            fy_cont = content[2:]
            reply_text = youdao_fy.get_fy(fy_cont)
            response = wechat_instance.response_text(content=reply_text)
        else:
            reply_date = tuling.get_tuling(content)
            if reply_date["code"] == 100000:
                reply_text = reply_date["text"]
                response = wechat_instance.response_text(content=reply_text)
            elif reply_date["code"] == 200000:
                reply_content = reply_date["text"]
                reply_url = "\n【<a href='{0}'>打开页面</a>】".format(reply_date["url"])
                reply_text = reply_content + reply_url
                response = wechat_instance.response_text(content=reply_text)
    
    return HttpResponse(response, content_type="application/xml")