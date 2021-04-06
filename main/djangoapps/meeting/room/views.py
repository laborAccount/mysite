#-*- coding: utf-8 -*-

import json
import asyncio
from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse, JsonResponse
from backend.djangoapps.common.util import views as TMUtility

#공통 API
from backend.djangoapps.common.com.views import CiscoApi
from backend.djangoapps.common.core.views import coreJson

from backend.models import CmsTemplate, CmsCospace
from django.db.models import Count, Q
import asyncio,datetime
import traceback
import logging

logger = logging.getLogger('sys')

# Author  : syh
# Desc    : MeetingRoom(cospace) 관리 페이지 로드
# History
def meetingroom(request):
    context = dict()
    return render(request, 'meeting/room/meetingRoom.html', context)

def meetingroom_list(request):
    context = dict()
    user_role = request.session['user_role']
    user_role = request.session['user_id']
    length = request.POST.get('length')
    draw = request.POST.get('draw')
    start = request.POST.get('start')
    searchText = request.POST.get('search[value]') # ??? search?

    cospace_list = list()           # context 리턴 Cospace List
    error_list = list()             # context 리턴 Error List
    total_list = list()             # MAX 값 구하는 용도

    

