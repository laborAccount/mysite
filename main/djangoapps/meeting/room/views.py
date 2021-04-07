#-*- coding: utf-8 -*-

import json
import asyncio
from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse, JsonResponse
from main.djangoapps.common.util import views as TMUtility

#공통 API
from main.djangoapps.common.com.views import CiscoApi
from main.djangoapps.common.core.views import coreJson

from main.models import CmsTemplate, CmsCospace
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
    length = request.POST.get('length') # T -> serverSide 옵션 true 시 시작 DataTable 한 페이지에 출력되는 row 개수
    draw = request.POST.get('draw') # T -> serverSide 옵션 true 시 시작 DataTable page 정보 
    start = request.POST.get('start') #T -> serverSide 옵션 true 시 시작 row번호 전송 
    searchText = request.POST.get('search[value]') # ??? search?

    cospace_list = list()           # context 리턴 Cospace List
    error_list = list()             # context 리턴 Error List
    total_list = list()             # MAX 값 구하는 용도

    query_param = dict()            # 페이징 
    query_param['limit'] = length
    query_param['offset'] = start

    if searchText != '' and searchText is not None :
        query_param['filter'] = searchText

    api_items = coreJson()['api'] #djangoapps.common.core.views에서 api.json값을 참조하여 api List[json 데이터] 를 반환
    ca = CiscoApi()

    total_list = list()
    #     api_items --> [
    #     {
    #         "api_list": [
    #             {
    #                 "ipAddress": "14.63.53.22",
    #                 "max_callLeg_total": "500",
    #                 "password": "Etechsystem",
    #                 "port": "449",
    #                 "seq": "0",
    #                 "serverName": "api_server_1",
    #                 "useHttps": "True",
    #                 "userName": "admin"
    #             },
    #             {
    #                 "ipAddress": "14.63.53.22",
    #                 "max_callLeg_total": "500",
    #                 "password": "Etechsystem",
    #                 "port": "449",
    #                 "seq": "1",
    #                 "serverName": "api_server_2",
    #                 "useHttps": "True",
    #                 "userName": "admin"
    #             }
    #         ],
    #         "group_name": "cluster1",
    #         "group_seq": "0"
    #       }
    #   ]
    for api_entity in api_items : # api_items 배열에서 첫 번쨰 json 개체 (json 데이터에 개체가 하나밖에 없음)
        ca.setGroupSeqData(api_entity) # ca 객체에 group_name , group_seq 셋팅
        
        for api_info in group_list['api_list']:
            ca.setServerSeqData(api_info['seq'])

            t_cospace_list = ca.comCallAPI('cospaces','GET',query_param=query_param) # comCallAPI 내부에서 requests를 통해 api에 요청(request)를 날려 JSON으로 가공된 값을 받아온다.
            # query_param -> 시작 row 번호, 한 화면에 보여줄 row 수 , search_Text (검색어) 정보

            if t_cospace_list['status'] == 200 :
                if t_cospace_list['total'] != 0 : 
                    total_list.append(t_cospace_list['total'])
                    for cospace_info in t_cospace_list['body']['coSpaces']['coSpace'] :
                        t_dict = dict()
                        t_dict = cospace_info
                        # 단순히 table 정보를 뿌려주는 연습 프로젝트임으로 서버와  그룹 정보까지 dictionary에 셋팅하지 않아본다.
                        #t_dict['server_name'] = t_cospace_list['server_name']
                        #t_dict['server_seq'] = t_cospace_list['server_seq']
                        #t_dict['group_seq'] = t_cospace_list['group_seq']
                        #t_dict['group_name'] = t_cospace_list['group_name']
            
                        # 정보가 없을시에 dict()정보를 빈 값으로 초기화
                        if 'name' not in cospace_info:
                            t_dict['name'] = ''

                        if 'uri' not in cospace_info:
                            t_dict['uri'] = ''

                        if 'secondaryUri' not in cospace_info:
                            t_dict['secondaryUri'] = ''

                        if 'callId' not in cospace_info:
                            t_dict['callId'] = ''

                        q_dict = TMUtility.query_args_escape(cospace_id=cospace_info['@id'])
                        query = '''
                            SELECT
                                a.cospace_id,
                                a.delete_yn,
                                a.regist_id,
                                b.user_role
                            FROM 
                                cms_cospace a 
                            LEFT JOIN 
                                cms_manager b
                            ON b.regist_id = a.regist_id
                            WHERE a.cospace_id = '{cospace_id}'
                            AND a.delete_yn = 'N'
                        '''.format(**q_dict)
                        query_list = TMUtility.get_query_to_list(query)
                        print("query_list  --->", query_list)
                        #if len(query_list) == 0:
                        #     t_dict['tm_create'] = 'N'
                        #     t_dict['owner_yn'] = 'N'
                        #else:
                        #    t_dict['tm_create'] = 'Y'
                        #    if user_role == 'A' or user_role == 'S':
                        #        t_dict['owner_yn'] = 'Y'
                        #    else:
                        #        if user_id == query_list[0]['regist_id']:
                        #            t_dict['owner_yn'] = 'Y'
                        #        else:
                        #            t_dict['owner_yn'] = 'N'
                        cospace_list.append(t_dict)

            
    total = max(total_list)
    context['result'] = 'success'
    context['data'] = cospace_list
    context['draw'] = draw
    context['recordsTotal'] = total
    context['recordsFiltered'] = total

    return JsonResponse(context)
