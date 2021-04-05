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


