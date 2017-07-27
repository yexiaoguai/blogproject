# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as django_settings

from wechat_sdk.basic import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

import meizu_weather, youdao_fy, tuling, os, random, sqlite3, time

WECHAT_TOKEN = "yeliangtoken870206"
AppID = "wx2611ba5d5e60a7f9"
AppSecret = "507b048cfdaebca74b723ee886091813"

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
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
            "您可以跟公众号机器人聊天，也可以通过以下的输入信息了解数据"
            "\n输入【天气xx】来查看xx天气的信息！ 例如输入：天气福州"
            "\n输入【翻译xx】将英文翻译成中文，也可以将中文翻译成英文！ 例如输入：翻译你好；或输入：翻译hello"
            "\n输入【房价】查看当日福州二手房房价信息，对房价走势判断有一定的判断"
            "\n输入【美女】查看美女图片！都是经过我精心挑选"
            "\n输入【帮助】查看更多的支持的功能"
            "\n后续我将开发出更多数据的查询，比如说中国经济数据查询（银行拆借利率等）"
            "\n当然我也会开通股票的龙虎榜信息等等！"
            "\n【<a href='http://119.29.143.106/getmovielist/'>我的电影收藏</a>】"
            ))

    if isinstance(message, TextMessage):
        # 当前的会话内容.
        content = message.content.strip()
        if content == "帮助":
            reply_text = (
                "您可以跟公众号机器人聊天，也可以通过以下的输入信息了解数据"
                "\n输入【天气xx】来查看xx天气的信息！ 例如输入：天气福州"
                "\n输入【翻译xx】将英文翻译成中文，也可以将中文翻译成英文！ 例如输入：翻译你好；或输入：翻译hello"
                "\n输入【房价】查看当日福州二手房房价信息，对房价走势判断有一定的判断"
                "\n输入【美女】查看美女图片！都是经过我精心挑选"
                "\n输入【帮助】查看更多的支持的功能"
                "\n后续我将开发出更多数据的查询，比如说中国经济数据查询（银行拆借利率等）"
                "\n当然我也会开通股票的龙虎榜信息等等！"
            )
            response = wechat_instance.response_text(content=reply_text)
        elif "天气" in content:
            city_name = content[2:]
            reply_text = meizu_weather.get_weather_data(city_name)
            response = wechat_instance.response_text(content=reply_text)
        elif "翻译" in content:
            fy_cont = content[2:]
            reply_text = youdao_fy.get_fy(fy_cont)
            response = wechat_instance.response_text(content=reply_text)
        elif content == "美女":
            filename = django_settings.MEDIA_ROOT+"/media_id.txt"
            # 从文件中读取图片的media_id.
            with open(filename, "r") as f:
                content = f.read()
            pic_list = content.split("\n")
            random_num = random.randint(0, len(pic_list)-1)
            response = wechat_instance.response_image(media_id=pic_list[random_num])
        elif content == "房价":
            house_db = django_settings.MEDIA_ROOT+"/house_data.db"
            conn = sqlite3.connect(house_db)
            cur = conn.cursor()

            date = time.strftime("%Y%m%d")
            sql = "select * from houses_data where date = '{0}'".format(date)
            cur.execute(sql)
            houses_count = cur.fetchall()[0][2]
            sql = "select * from houses_data where date = '{0}'".format(date)
            cur.execute(sql)
            houses_aver_price = cur.fetchall()[0][1]
            # 鼓楼区
            sql = "select * from houses_data where date = '{0}'".format(date)
            cur.execute(sql)
            gulou_count = cur.fetchall()[0][6]
            sql = "select * from houses_data where date = '{0}'".format(date)
            cur.execute(sql)
            gulou_aver_price = cur.fetchall()[0][5]
            # 台江区
            sql = "select * from houses_data where date = '{0}'".format(date)
            cur.execute(sql)
            taijiang_count = cur.fetchall()[0][4]
            sql = "select * from houses_data where date = '{0}'".format(date)
            cur.execute(sql)
            taijiang_aver_price = cur.fetchall()[0][3]

            reply_text = "福州二手房【{0}】数据：\n挂牌出售数量：{1}套。\n挂牌出售均价：{2}元。\
                \n鼓楼区二手房挂牌出售数量：{3}套。\n挂牌出售均价：{4}元。\
                \n台江区二手房挂牌出售数量：{5}套。\n挂牌出售均价：{6}元。\
                \n以上数据均不包含别墅。"\
                .format(date, int(houses_count), round(houses_aver_price, 2), 
                        int(gulou_count), round(gulou_aver_price, 2),
                        int(taijiang_count), round(taijiang_aver_price, 2))

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