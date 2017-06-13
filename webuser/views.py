# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    user = request.user
    return render(request, "webuser/index.html")
