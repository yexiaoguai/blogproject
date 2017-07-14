#!/usr/bin/env python
#coding:utf-8

import json, requests

URL = "http://fanyi.youdao.com/translate?doctype=json"

def get_fy_data(word):
    post_data = {"i":word}
    html_bytes = requests.post(URL, data=post_data)
    return html_bytes.text

def get_fy(word):
    content = get_fy_data(word)
    data = json.loads(content)
    json_errorCode = data["errorCode"]
    if json_errorCode == 0:
        newdata = data["translateResult"]
        result_str = ""
        for tgt_list in newdata:
            for tgt in tgt_list:
                result_str += tgt["tgt"]
            result_str += "\n"
    else:
        return "翻译失败！"
    return result_str
     
