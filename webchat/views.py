# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

from webuser.forms import LoginForm
from webuser.models import Webuser

import json, Queue, datetime, threading 

GLOBAL_MQ = {}

def webchat(request):
    """
    聊天的视图函数.
    """
    action = "webchat"
    if request.user.is_authenticated:
        return render(request, "webchat/webchat.html", {"action":action})
    else:
        return render(request, "webuser/login.html", {"form":LoginForm()})

def contacts(request):
    contact_dic = {}
    # 连表查询.
    contacts = request.user.webuser.friends.select_related().values("id", "user__username", "online")
    # print "contacts 1 : ", contacts
    for i in contacts:
        webuser = Webuser.objects.get(pk=i["id"])
        i["pictures"] = webuser.get_picture()
    # print "contacts 2 : ", contacts
    contact_dic["contact_list"] = list(contacts)
    # print "contact_dic : ", contact_dic

    # groups = request.user.webuser.chatgroup_set.select_related().values("id", "name", "memberlimits")
    # print "groups : ", groups
    # contact_dic["group_list"] = list(groups)

    return HttpResponse(json.dumps(contact_dic))

class CustomTask:
    def __init__(self):
        self._result = None
    
    def run(self, request):
        # 你的代码, 你用来进行多线程
        request_user_webuser_id = str(request.user.webuser.id)
        message_list = []
        # 判断下id在不在全局
        if request_user_webuser_id in GLOBAL_MQ:
            # 用户的webuser_id对应的的消息数量.
            stored_ms_nums = GLOBAL_MQ[request_user_webuser_id].qsize()
            if stored_ms_nums == 0:
                try:
                    # GLOBAL_MQ[request_user_webuser_id]是一个Queue对象
                    # get方法将第一个值从队列取出
                    # 加入message_list里面
                    message_list.append(GLOBAL_MQ[request_user_webuser_id].get(timeout=15))
                except Exception as e:
                    print "ERROR is : ", e
            for i in range(stored_ms_nums):
                # print "range : ", i
                message_list.append(GLOBAL_MQ[request_user_webuser_id].get())
        else:
            # 创建一个队列对象
            GLOBAL_MQ[request_user_webuser_id] = Queue.Queue()
        result = HttpResponse(json.dumps(message_list))
        self._result = result
    
    def get_result(self):
        return self._result

def newmessage(request):
    if request.method == "POST":
        # print "request : ", request.POST.get("data")
        data = json.loads(request.POST.get("data"))
        # print "data : ", data
        # send_to就是request.user.webuser.id
        send_to = data["to"]
        if send_to not in GLOBAL_MQ:
            GLOBAL_MQ[send_to] = Queue.Queue()
        data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 存入聊天信息到队列中
        GLOBAL_MQ[send_to].put(data)
        # print "GLOBAL_MQ : ", GLOBAL_MQ
        return HttpResponse(GLOBAL_MQ[send_to].qsize())

    # 打开webchat/newmessage/网页就会加载这个视图函数.
    else:
        ct = CustomTask()
        thread = threading.Thread(target=ct.run, args=(request,))    #args传参
        thread.start()
        thread.join()
        return ct.get_result()