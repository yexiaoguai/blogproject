#!/usr/bin/env python
#coding:utf-8

import json, sys, requests

URL = "http://www.tuling123.com/openapi/api"
APIKEY = "3eba69e496c444a3b933f396726088c8"
USERID = "ABC123"

def get_context(info):
    post_data = {"key":APIKEY, "info":info, "userid":USERID}
    rep = requests.post(URL, data=post_data)
    return rep.text

def get_tuling(info):
    """
    100000	文本类
    200000	链接类
    302000	新闻类
    308000	菜谱类
    """
    return_data = {}
    rep = get_context(info)
    data = json.loads(rep)
    json_code = data["code"]
    if json_code == 100000:
        return_data["code"] = data["code"]
        return_data["text"] = data["text"]
    elif json_code == 200000:
        return_data["code"] = data["code"]
        return_data["text"] = data["text"]
        return_data["url"] = data["url"]

    return return_data