# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.basic import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

WECHAT_TOKEN = "yeliangtoken870206"

wechat_instance = WechatBasic(token=WECHAT_TOKEN)

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
            '感谢您的关注！\n回复【help】查看支持的功能'
            '\n【<a href="http://119.29.143.106/getmovielist/">我的电影收藏</a>】'
            ))

    if isinstance(message, TextMessage):
        # 当前的会话内容.
        content = message.content.strip()
        if content == "help":
            reply_text = (
                "输入【股票】来查看大盘今天重要的数据！"
            )
        response = wechat_instance.response_text(content=reply_text)
    
    return HttpResponse(response, content_type="application/xml")