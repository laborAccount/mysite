# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from main.models import CmsEndpointGroup
from main.models import CmsManager

# api 공통
from main.djangoapps.common.api.views import callApi, callApiBasic, callApi_server, callApiId
from main.djangoapps.common.api.views import api_data_list, api_data_list_basic, api_data_list_basic_server
from main.djangoapps.common.api.views import request_to_json
from main.djangoapps.common.core.views import coreJson
from main.djangoapps.common.com.views import CiscoApi
import asyncio
from time import time
from django.db import connections

import re

def get_query_to_list(query):
    data_list = list()
    with connections['default'].cursor() as cur:
        cur.execute(query)
        col_names = [desc[0] for desc in cur.description]

        while True:
            row = cur.fetchone()
            if row is None:
                break
            row_dict = dict(zip(col_names, row))
            data_list.append(row_dict)

        cur.close()

    return data_list


def get_query_to_dict(query):
    data_dict = dict()

    with connections['default'].cursor() as cur:
        cur.execute(query)
        col_names = [desc[0] for desc in cur.description]

        while True:
            row = cur.fetchone()
            if row is None:
                break
            data_dict = dict(zip(col_names, row))

        cur.close()

    return data_dict

def execute_query(query,lastrowflag=None):
    ret_rowid = None
    with connections['default'].cursor() as cur:
        cur.execute(query)
        if lastrowflag is not None:
            ret_rowid = cur.lastrowid
        cur.close()

    if lastrowflag is not None:
        return ret_rowid

def query_args_escape(**kwargs):
    
    ret_dict = dict()
    
    for key,value in kwargs.items():
        if type(value) == type(str()):
            value = re.sub('[\']', '\\\'', value)
            ret_dict[key] = value
        else :
            ret_dict[key] = value

    return ret_dict

# api 공통
from main.djangoapps.common.com.views import CiscoApi
import asyncio


def searchUser(request):
    searchEmail = request.POST.get('searchEmail')

    ca = CiscoApi()
    acano_list = list()
    context = dict()
    api_list = coreJson()['api']
    query_param = dict()

    temp_user_list = list()

    for group_list in api_list:
        temp_dict = dict()
        ca.setGroupSeq(group_list['group_seq'])

        for group_data in group_list['api_list']:
            ca.setServerSeqData(group_data['seq'])
            query_param['filter'] = searchEmail
            context_temp = ca.comCallAPI('users', "GET", query_param=query_param)
            if context_temp['status'] == 200:
                if context_temp['total'] > 0:
                    if context_temp['total'] == 1:
                        temp_dict = dict()
                        temp_dict['user'] = context_temp['body']['users']['user']
                        temp_dict['group_seq'] = group_list['group_seq']
                        temp_dict['server_seq'] = group_data['seq']
                        temp_user_list.append(temp_dict)
                    else:
                        for temp in context_temp['body']['users']['user']:
                            temp_dict = dict()
                            temp_dict['user'] = temp
                            temp_dict['group_seq'] = group_list['group_seq']
                            temp_dict['server_seq'] = group_data['seq']
                            temp_user_list.append(temp_dict)

    loop = asyncio.new_event_loop()
    temp_list = loop.run_until_complete(searchUser_sub_1(loop, temp_user_list))
    loop.close()

    ret_list = []

    for i in range(0, len(temp_list)):
        if temp_list[i] not in temp_list[i + 1:]:
            ret_list.append(temp_list[i])

    context['data'] = ret_list

    return JsonResponse({'return': context})


async def searchUser_sub_1(loop, temp_user_list):
    futures = [asyncio.ensure_future(searchUser_sub_1_fetch(loop, temp_user)) for temp_user in temp_user_list]
    result = await asyncio.gather(*futures)
    return result


async def searchUser_sub_1_fetch(loop, temp_user):
    retData = await loop.run_in_executor(None, searchUser_sub_1_call_api, temp_user)
    return retData


def searchUser_sub_1_call_api(temp_user):
    ca = CiscoApi()
    ca.setGroupSeq(temp_user['group_seq'])
    ca.setServerSeqData(temp_user['server_seq'])
    temp_result = ca.comCallAPI('users/{id}'.format(id=temp_user['user'][0]['@id']), "GET")
    reData = dict()
    if temp_result['status'] == 200:
        reData['id'] = temp_result['body']['user']['@id']
        reData['userJid'] = temp_result['body']['user']['userJid']
        reData['name'] = temp_result['body']['user']['name']
        reData['email'] = temp_result['body']['user']['email']
        reData['tenant'] = temp_result['body']['user']['tenant'] if 'tenant' in temp_result['body']['user'] else ''

    return reData


def tm_event_log(request,p_uri=None,p_data=None,success_yn=None,p_type=None,p_comment=None,p_error=None):
    
    
    try:
        with connections['default'].cursor() as cur:
            
            query = '''
                 INSERT INTO cms_event_log (tm_type, tm_uri, tm_param, tm_comment, tm_error, success_yn, user_id, fst_regr_id, fnl_mdfr_id) VALUES ('{tm_type}','{tm_url}','{tm_param}','{tm_comment}','{tm_error}','{success_yn}','{user_id}','{fst_regr_id}','{fnl_mdfr_id}')
            '''.format(tm_type=p_type,tm_url=p_uri,tm_param=p_data,tm_comment=p_comment,tm_error=p_error,success_yn=success_yn,user_id=request.session['user_id'],fst_regr_id=request.session['user_id'],fnl_mdfr_id=request.session['user_id'])
            cur.execute(query)
            cur.close()


    except BaseException as e:
        print("오류: ",e)
    

def get_error_message(temp_data):
    for data in temp_data.errors:
        if type(data) == str:
            if type(temp_data.errors[data]) == list:
                for data2 in temp_data.errors[data]:
                    if type(data2) == dict:
                        for key in data2:
                            for temp_data in data2[key]: 
                                return temp_data
                    else:
                        for temp_data in temp_data.errors[data]:
                            return temp_data
            else:
                for temp_key in temp_data.errors[data]:
                    if type(temp_key) == str:
                        if type(temp_data.errors[data][temp_key]) == list:
                            for temp_data in temp_data.errors[data][temp_key]:
                                return temp_data