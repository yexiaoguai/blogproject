#!/usr/bin/env python
#coding:utf-8

import json, sys, requests

URL = "http://aider.meizu.com/app/weather/listWeather?cityIds="

def get_cityid(city_name):
    # 从文件中读取需要更新的电影名称.
    with open("Meizu_cities.json", "r") as f:
        content = f.read()
    data = json.loads(content)
    list_city_info = data["cities"]
    for city_info in list_city_info:
        if city_info["countyname"] == city_name:
            return city_info["areaid"]

    return "查询失败！"

def get_weather_meizu(city_ids):
    url = URL + city_ids
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    html_bytes = requests.get(url, headers=header)
    return html_bytes.text

def get_weather_data(city_name):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # name = "福州"
    id = get_cityid(city_name)
    content = get_weather_meizu(str(id))

    data = json.loads(content)
    json_data = json.dumps(data["value"])
    # str砍头去尾
    json_data = json_data[1:-1]
    newdata = json.loads(json_data)
    city_name = newdata["city"]
    province_name = newdata["provinceName"]

    city_25 = newdata["pm25"]
    city_aqi = city_25["aqi"]
    city_quality = city_25["quality"]
    city_25_num = city_25["pm25"]
    city_10_num = city_25["pm10"]

    city_weathers = newdata["weathers"]
    city_weather_date = city_weathers[0]["date"]
    city_weather = city_weathers[0]["weather"]
    city_temp_day_c = city_weathers[0]["temp_day_c"]
    city_temp_night_c = city_weathers[0]["temp_night_c"]
    city_sun_down_time = city_weathers[0]["sun_down_time"]
    city_sun_rise_time = city_weathers[0]["sun_rise_time"]

    city_indexes = newdata["indexes"]
    for info in city_indexes:
        if info["abbreviation"] == "gm":
            info_gm = info["content"]
            print "感冒指数: ", info_gm
        if info["abbreviation"] == "pp":
            info_pp = info["content"]
            print "化妆指数: ", info_pp
        if info["abbreviation"] == "zs":
            info_zs = info["content"]
            print "中暑指数: ", info_zs
        if info["abbreviation"] == "ys":
            info_ys = info["content"]
            print "雨伞指数: ", info_ys
        if info["abbreviation"] == "yh":
            info_yh = info["content"]
            print "约会指数: ", info_yh
        if info["abbreviation"] == "yd":
            info_yd = info["content"]
            print "运动指数: ", info_yd
        if info["abbreviation"] == "xq":
            info_xq = info["content"]
            print "心情指数: ", info_xq
        if info["abbreviation"] == "xc":
            info_xc = info["content"]
            print "洗车指数: ", info_xc
        if info["abbreviation"] == "wc":
            info_wc = info["content"]
            print "风寒指数: ", info_wc
        if info["abbreviation"] == "uv":
            info_uv = info["content"]
            print "紫外线强度指数: ", info_uv
        if info["abbreviation"] == "tr":
            info_tr = info["content"]
            print "旅游指数: ", info_tr
        if info["abbreviation"] == "pl":
            info_pl = info["content"]
            print "空气污染扩散条件指数: ", info_pl
        if info["abbreviation"] == "fs":
            info_fs = info["content"]
            print "防晒指数: ", info_fs
        if info["abbreviation"] == "ct":
            info_ct = info["content"]
            print "穿衣指数: ", info_ct
        if info["abbreviation"] == "ac":
            info_ac = info["content"]
            print "空调开启指数: ", info_ac
        

    str_weather = "【{0}，{1}】\n【白天气温】: {2}摄氏度\n【夜间气温】: {3}摄氏度\n"\
                  "【日出时间】: {4}\n"\
                  "【日落时间】: {5}\n"\
                  "【空气质量】: {6}\n"\
                  "【空气质量指数】: {7}\n"\
                  "【PM25指数】: {8}\n"\
                  "【PM10指数】: {9}\n"\
                  "【感冒指数】: {10}\n"\
                  "【紫外线强度指数】: {11}\n"\
                  "【穿衣指数】: {12}\n"\
                  "【化妆指数】: {13}\n"\
                  "【运动指数】: {14}\n"\
                .format(province_name, city_name, city_temp_day_c, city_temp_night_c,
                city_sun_rise_time, city_sun_down_time, city_quality, city_aqi,
                city_25_num, city_10_num, info_gm, info_uv, info_ct, info_pp, info_yd)

    return str_weather


