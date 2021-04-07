# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.conf import settings
from main.djangoapps.common.core.views import getAuthToken, getAuthTokenBasic
from main.djangoapps.common.core.views import getApiUrl, getApiUrlBasic
from main.djangoapps.common.core.views import getUseHttps, getUseHttpsBasic
from main.djangoapps.common.core.views import getErrorJson
from main.djangoapps.common.core.views import coreJson
import logging
import logging.config
# UTIL
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import xmltodict


def callApiBasic(url, jsonParam, type):
    retData = {}
    try:
        Authorization = getAuthTokenBasic()
        apiUrl = getApiUrlBasic()
        useHttps = getUseHttpsBasic()

        fullurl = ""

        if useHttps is True:
            fullurl = "https://"
        else:
            fullurl = "http://"

        fullurl = fullurl + apiUrl + '/api/v1/' + url
        headers = {
            'Authorization': Authorization
        }
        res = ""
        if type == "GET":
            res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
        elif type == "POST":
            res = requests.post(fullurl, headers=headers, verify=False, data=jsonParam)
        elif type == "PUT":
            res = requests.put(fullurl, headers=headers, verify=False, data=jsonParam)
        elif type == "DELETE":
            res = requests.delete(fullurl, headers=headers, verify=False, data=jsonParam)

        res.encoding = 'UTF-8'

        retData = {}
        retData['headers'] = res.headers
        retData['body'] = api_data_to_json(res.text)
        # 예외 발생 에러
        retData['error'] = ''
        retData['status'] = res.status_code

        if res.status_code != 200:
            if res.status_code == 400:
                # xml to json
                o = xmltodict.parse(res.text)
                errorData = json.dumps(o)
                errorJson = json.loads(errorData)
                defKeyJson = getErrorJson()
                defKeys = defKeyJson['failureDetails'].keys()

                # Api Error Message 정리후 메시지 전송
                errorKeys = list(errorJson['failureDetails'].keys())

                if errorKeys[0] in defKeys:
                    retData['error'] = errorKeys[0]

            elif res.status_code == 401:
                # Unauthorized (권한없음)
                retData['error'] = '401 Unauthorized'

            elif res.status_code == 404:
                retData['error'] = '404 Not Found'

            # 통신 장애등 기타 장애에 대한 처리
            # retData['body'] =
            # retData['error'] =
            # retData['headers'] =

    except BaseException as e:
        # log 파일에 에러 내용 추가 예정
        retData['status'] = 99999
        retData['error'] = '알 수 없는 에러가 발생하였습니다.'

    return retData


# from backend.djangoapps.common.api.views import callApi
def callApi(url, jsonParam, type, server_seq=None):
    try:
        api_json = coreJson()
        api_list = list()
        res = ""
        for idx, server in enumerate(api_json['api'], 1):
            Authorization = getAuthToken(server['userName'], server['password'])
            apiUrl = getApiUrl(server['ipAddress'], server['port'])
            useHttps = getUseHttps(server['useHttps'])

            fullurl = ""

            if useHttps is True:
                fullurl = "https://"
            else:
                fullurl = "http://"

            fullurl = fullurl + apiUrl + '/api/v1/' + url
            headers = {
                'Authorization': Authorization
            }

            if type == "GET":
                if server_seq is None:
                    res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                    res_json = api_status_data(res)

                    if res_json['status'] == 200:
                        # 한 서버의 모든 데이터를 가져오는 함수 실행
                        list_data = api_data_list(fullurl, int(res_json['body'][url]['@total']), url, headers,
                                                  server['seq'])
                        api_list.extend(list_data)
                    if idx == len(api_json['api']):
                        # 전체 api 데이터를 중복제거
                        api_list = list({data['@id']: data for data in api_list}.values())
                        retData = {'error': res_json['error'], 'body': api_list, 'status': res.status_code}
                        return retData

                    continue
                elif server_seq == server['seq']:
                    res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                else:
                    continue
            elif type == "POST" and server['seq'] == server_seq:
                res = requests.post(fullurl, headers=headers, verify=False, data=jsonParam)
            elif type == "PUT" and server['seq'] == server_seq:
                res = requests.put(fullurl, headers=headers, verify=False, data=jsonParam)
            elif type == "DELETE" and server['seq'] == server_seq:
                res = requests.delete(fullurl, headers=headers, verify=False, data=jsonParam)

            retData = api_status_data(res, server['seq']) if res != '' else ''

    except BaseException as e:
        # log 파일에 에러 내용 추가 예정
        retData = dict()
        retData['status'] = 99999
        retData['error'] = '알 수 없는 에러가 발생하였습니다.'

        return retData

    return retData


# api 통신 결과 처리 함수
# from backend.djangoapps.common.api.views import api_status_data
def api_status_data(res, server_seq=None):
    res.encoding = 'UTF-8'
    retData = {}
    retData['headers'] = res.headers
    retData['body'] = api_data_to_json(res.text)
    # 예외 발생 에러
    retData['error'] = ''
    retData['status'] = res.status_code
    # retData['server_seq'] = server_seq

    if res.status_code != 200:
        if res.status_code == 400:
            # xml to json
            errorJson = api_data_to_json(res.text)
            defKeyJson = getErrorJson()
            defKeys = defKeyJson['failureDetails'].keys()

            # Api Error Message 정리후 메시지 전송
            errorKeys = list(errorJson['failureDetails'].keys())

            if errorKeys[0] in defKeys:
                retData['error'] = errorKeys[0]

        elif res.status_code == 401:
            # Unauthorized (권한없음)
            retData['error'] = '401 Unauthorized'

        elif res.status_code == 404:
            retData['error'] = '404 Not Found'

    return retData


# list 출력시 total 값으로 전체 데이터를 만드는 함수
def api_data_list_basic(url, total, data_key):
    call_cnt = int(total / 20 + 1) if total % 20 != 0 and total != 0 else int(total / 20)
    res_list = list()
    for n in range(0, call_cnt):
        call_uri = url + '?offset={offset}&limit=20'.format(offset=n * 20)
        res_json = callApiBasic(call_uri, None, 'GET')
        # 데이터가 여러건인 경우와 단건인 경우를 나눠서 처리
        if type(res_json['body'][data_key][data_key[:-1]]) is list:
            res_list.append(res_json['body'][data_key][data_key[:-1]])
        else:
            res_list.append([res_json['body'][data_key][data_key[:-1]]])

    tot_res_list = [data for rows in res_list for data in rows]
    return tot_res_list


# CMS Client Datatable serverside 통신
def api_data_list_basic_server(url, start, data_key):
    # offset=pagenum-1 limit=10으로 고정
    offset = start
    # call_cnt ===> page number
    # limit = 10고정
    # offset = start
    res_list = list()
    call_uri = url + '?offset={offset}&limit=10'.format(offset=start)
    res_json = callApiBasic(call_uri, None, 'GET')
    res_list.append(res_json['body'][data_key][data_key[:-1]])
    tot_res_list = [data for rows in res_list for data in rows]
    return tot_res_list


# from backend.djangoapps.common.api.views import callApi MeetingRoom serverside 통신
def callApi_server(url, jsonParam, type, start=None, server_seq=None, addparam=None):
    try:
        api_json = coreJson()
        api_list = list()
        res = ""

        for idx, server in enumerate(api_json['api'], 1):
            Authorization = getAuthToken(server['userName'], server['password'])
            apiUrl = getApiUrl(server['ipAddress'], server['port'])
            useHttps = getUseHttps(server['useHttps'])

            fullurl = ""

            if useHttps is True:
                fullurl = "https://"
            else:
                fullurl = "http://"

            fullurl = fullurl + apiUrl + '/api/v1/' + url
            headers = {
                'Authorization': Authorization
            }

            if type == "GET":
                if server_seq is None:
                    res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                    res_json = api_status_data(res)

                    if res_json['status'] == 200:
                        # 한 서버의 모든 데이터를 가져오는 함수 실행
                        if addparam is None:
                            list_data = api_data_list_server(fullurl, start, url, headers, server['seq'])

                        else:
                            list_data = api_data_list_server(fullurl, start, url, headers, server['seq'],
                                                             addparam=addparam)

                        api_list.extend(list_data)

                    if idx == len(api_json['api']):
                        # 전체 api 데이터를 중복제거
                        api_list = list({data['@id']: data for data in api_list}.values())
                        retData = {'error': res_json['error'], 'body': api_list, 'status': res.status_code,
                                   'total': len(api_list)}
                        return retData

                    continue
                elif server_seq == server['seq']:
                    res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                    res_json = api_status_data(res)
                    # res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                    if addparam is None:
                        list_data = api_data_list_server(fullurl, start, url, headers, server['seq'])
                        retData = {'error': res_json['error'], 'body': list_data, 'status': res.status_code,
                                   'total': len(list_data)}
                        return retData

                    else:
                        list_data = api_data_list_server(fullurl, start, url, headers, server['seq'], addparam=addparam)

                else:
                    continue
            elif type == "POST" and server['seq'] == server_seq:
                res = requests.post(fullurl, headers=headers, verify=False, data=jsonParam)
            elif type == "PUT" and server['seq'] == server_seq:
                res = requests.put(fullurl, headers=headers, verify=False, data=jsonParam)
            elif type == "DELETE" and server['seq'] == server_seq:
                res = requests.delete(fullurl, headers=headers, verify=False, data=jsonParam)

            retData = api_status_data(res, server['seq']) if res != '' else ''
    except BaseException as e:
        # log 파일에 에러 내용 추가 예정
        retData = dict()
        retData['status'] = 99999
        retData['error'] = '알 수 없는 에러가 발생하였습니다.'
        return retData
    return retData


# from backend.djangoapps.common.api.views import api_data_list serverside 통신
def api_data_list_server(url, start, data_key, headers, server_seq=None, addparam=None):
    offset = start
    try:
        res_list = list()
        call_uri = url + '?offset={offset}&limit=10'.format(offset=offset)
        # api 직접 호출
        if addparam is not None:
            call_uri = call_uri + addparam
        res_json = requests.get(call_uri, headers=headers, verify=False)
        retData = api_status_data(res_json, server_seq)

        if retData['status'] == 200:
            # 데이터가 여러건인 경우와 단건인 경우를 나눠서 처리
            if int(retData['body'][data_key]['@total']) == 0:
                tot_res_list = {}
            else:
                if type(retData['body'][data_key][data_key[:-1]]) is list:
                    for data in retData['body'][data_key][data_key[:-1]]:
                        data['server_seq'] = server_seq
                    res_list.append(retData['body'][data_key][data_key[:-1]])
                else:
                    retData['body'][data_key][data_key[:-1]]['server_seq'] = server_seq
                    res_list.append([retData['body'][data_key][data_key[:-1]]])

                tot_res_list = [data for rows in res_list for data in rows]
    except BaseException as e:
        tot_res_list = {}
    return tot_res_list


# from backend.djangoapps.common.api.views import api_data_list
def api_data_list(url, total, data_key, headers, server_seq=None):
    call_cnt = int(total / 10 + 1) if total % 10 != 0 and total != 0 else int(total / 10)

    res_list = list()
    for n in range(0, call_cnt):
        call_uri = url + '?offset={offset}&limit=10'.format(offset=n * 10)
        # api 직접 호출
        res_json = requests.get(call_uri, headers=headers, verify=False)
        retData = api_status_data(res_json, server_seq)

        if retData['status'] == 200:
            # 데이터가 여러건인 경우와 단건인 경우를 나눠서 처리
            if type(retData['body'][data_key][data_key[:-1]]) is list:
                for data in retData['body'][data_key][data_key[:-1]]:
                    data['server_seq'] = server_seq
                res_list.append(retData['body'][data_key][data_key[:-1]])
            else:
                retData['body'][data_key][data_key[:-1]]['server_seq'] = server_seq
                res_list.append([retData['body'][data_key][data_key[:-1]]])

    tot_res_list = [data for rows in res_list for data in rows]

    return tot_res_list


# get으로 호출한 데이터를 json 형식으로 변환하는 함수
# from backend.djangoapps.common.api.views import api_data_to_json
def api_data_to_json(res_txt):
    if res_txt is not '':
        o = xmltodict.parse(res_txt)
        res_data = json.dumps(o)
        res_json = json.loads(res_data)

        return res_json


# POST, PUT request를 json으로 변환하는 함수
# from backend.djangoapps.common.api.views import request_to_json
def request_to_json(post_data):
    json_data = json.dumps(post_data)
    json_data = json.loads(json_data)
    return json_data


# from backend.djangoapps.common.api.views import api_coSpaces_POST
def api_coSpaces_POST_JSON(request):
    json_data = json.dumps(request)
    json_data = json.loads(json_data)

    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/coSpaces'
    headers = {
        'Authorization': Authorization
    }

    r = requests.post(url, headers=headers, verify=False, data=json_data)

    # r = callApi("coSpaces",json_data,"POST")

    return r


def api_coSpaces_POST(request):
    json_data = json.dumps(request.POST)
    json_data = json.loads(json_data)

    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/coSpaces'
    headers = {
        'Authorization': Authorization
    }

    r = requests.post(url, headers=headers, verify=False, data=json_data)

    return r


# from backend.djangoapps.common.api.views import api_coSpaces
def api_coSpaces():
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/coSpaces'
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    requestCnt = (int(resDataJson['coSpaces']['@total']) / 20) + 1 if (int(
        resDataJson['coSpaces']['@total']) % 20) != 0 else int(resDataJson['coSpaces']['@total']) / 20

    resDataList = list()

    for n in range(0, int(requestCnt)):
        url = 'https://' + apiUrl + '/api/v1/coSpaces?offset={offset}&limit=20'.format(offset=n * 20)
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'UTF-8'
        res_data = str(res.text)
        res_o = xmltodict.parse(res_data)
        res_data = json.dumps(res_o)
        res_data_json = json.loads(res_data)

        if type(res_data_json['coSpaces']['coSpace']) == list:
            resDataList.append(res_data_json['coSpaces']['coSpace'])
        else:
            single_data = [res_data_json['coSpaces']['coSpace']]
            resDataList.append(single_data)

    totDataList = list()
    for list_data in resDataList:
        for data in list_data:
            totDataList.append(data)

    for n in range(0, len(totDataList)):
        if 'uri' not in totDataList[n]:
            totDataList[n]['uri'] = ''
        if 'secondaryUri' not in totDataList[n]:
            totDataList[n]['secondaryUri'] = ''
        if 'cdrTag' not in totDataList[n]:
            totDataList[n]['cdrTag'] = ''

    return totDataList


# from backend.djangoapps.common.api.views import api_coSpaceId
def api_coSpaceId_JSON(id, request=None):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/coSpaces/' + id
    headers = {
        'Authorization': Authorization


    }
    if request is not None:
        json_data = json.dumps(request)
        json_data = json.loads(json_data)
        resDataJson = requests.put(url, headers=headers, verify=False, data=json_data)

    else:
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = 'UTF-8'
        resData = str(r.text)

        # xml to json
        o = xmltodict.parse(resData)
        resData = json.dumps(o)
        resDataJson = json.loads(resData)

    return resDataJson


def api_coSpaceId(id, request=None):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/coSpaces/' + id
    headers = {
        'Authorization': Authorization
    }
    if request is not None:
        json_data = json.dumps(request.POST)
        json_data = json.loads(json_data)
        resDataJson = requests.put(url, headers=headers, verify=False, data=json_data)

    else:
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = 'UTF-8'
        resData = str(r.text)

        # xml to json
        o = xmltodict.parse(resData)
        resData = json.dumps(o)
        resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_coSpaceDel
def api_coSpaceDel(request):
    coSpaceId_list = request.POST.getlist('del_arr[]')
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    headers = {
        'Authorization': Authorization
    }
    error_id = list()
    for coSpaceId in coSpaceId_list:
        url = 'https://' + apiUrl + '/api/v1/coSpaces/' + coSpaceId
        r = requests.delete(url, headers=headers, verify=False)
        r.encoding = 'UTF-8'

        if r.status_code != 200:
            error_id.append(r)

    return error_id


# from backend.djangoapps.common.api.views import api_activeCall
def api_activeCall(callstatus=None):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/calls'
    headers = {
        'Authorization': Authorization
    }

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    if callstatus is not None:
        return resDataJson

    requestCnt = (int(resDataJson['calls']['@total']) / 20) + 1 \
        if (int(resDataJson['calls']['@total']) % 20) != 0 \
        else int(resDataJson['calls']['@total']) / 20

    resDataList = list()

    for n in range(0, int(requestCnt)):
        url = 'https://' + apiUrl + '/api/v1/calls?offset={offset}&limit=20'.format(offset=n * 20)
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'UTF-8'
        res_data = str(res.text)
        res_o = xmltodict.parse(res_data)
        res_data = json.dumps(res_o)
        res_data_json = json.loads(res_data)
        if type(res_data_json['calls']['call']) == list:
            resDataList.append(res_data_json['calls']['call'])
        else:
            single_data = [res_data_json['calls']['call']]
            resDataList.append(single_data)

    totDataList = list()
    for list_data in resDataList:
        for data in list_data:
            totDataList.append(data)

    return totDataList


# from backend.djangoapps.common.api.views import api_activeCallId
def api_activeCallId(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/calls/' + id

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_activeCallId_delete
def api_activeCallId_delete(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/calls/' + id

    r = requests.delete(url, headers=headers, verify=False)

    return r


# from backend.djangoapps.common.api.views import api_activeCallId_add
def api_activeCallId_add(request):
    json_data = json.dumps(request.POST)
    json_data = json.loads(json_data)
    Authorization = getAuthTokenBasic()
    apiUrl = getApiUrlBasic()

    url = 'https://' + apiUrl + '/api/v1/calls'
    headers = {
        'Authorization': Authorization
    }

    r = requests.post(url, headers=headers, verify=False, data=json_data)

    return r


# from backend.djangoapps.common.api.views import api_callLegs
def api_callLegs(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/callLegs/' + id

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    if r.status_code != 404:
        resData = str(r.text)

        # xml to json
        o = xmltodict.parse(resData)
        resData = json.dumps(o)
        resDataJson = json.loads(resData)

        return resDataJson
    else:
        return r.status_code


# from backend.djangoapps.common.api.views import api_callLegs_update
def api_callLegs_update(request, call_id=None):
    id = request.POST.get('user_api_id') if call_id is None else call_id
    user_key = request.POST.get('user_key')
    user_value = request.POST.get('user_value')
    put_data = {user_key: user_value}
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/callLegs/' + id

    r = requests.put(url, headers=headers, verify=False, data=put_data)
    r.encoding = 'UTF-8'

    error_id = list()

    if r.status_code != 200:
        error_id.append(r)

    return error_id


# from backend.djangoapps.common.api.views import api_callLegs_delete
def api_callLegs_delete(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/callLegs/' + id

    r = requests.delete(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'

    error_id = list()

    if r.status_code != 200:
        error_id.append(r)

    return error_id


# from backend.djangoapps.common.api.views import api_callLegProfiles_POST
def api_callLegProfiles_POST(callLegProfiles_data):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/callLegProfiles'
    headers = {
        'Authorization': Authorization
    }

    r = requests.post(url, headers=headers, verify=False, data=callLegProfiles_data)

    return r


# from backend.djangoapps.common.api.views import api_callLegProfiles_Id
def api_callLegProfiles_Id(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/callLegProfiles/' + id
    headers = {
        'Authorization': Authorization
    }

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_callLegProfiles_Update
def api_callLegProfiles_Update(id, callLegProfiles_data):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/callLegProfiles/' + id
    headers = {
        'Authorization': Authorization
    }

    res = requests.put(url, headers=headers, verify=False, data=callLegProfiles_data)

    return res


# from backend.djangoapps.common.api.views import api_callLegProfiles_Delete
def api_callLegProfiles_Delete(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/callLegProfiles/' + id
    r = requests.delete(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'

    return r


# from backend.djangoapps.common.api.views import api_callProfiles_POST
def api_callProfiles_POST(callProfiles_data):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/callProfiles'
    headers = {
        'Authorization': Authorization
    }

    r = requests.post(url, headers=headers, verify=False, data=callProfiles_data)

    return r


# from backend.djangoapps.common.api.views import api_callProfiles_Id
def api_callProfiles_Id(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/callProfiles/' + id
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_callProfiles_Update
def api_callProfiles_Update(id, callProfiles_data):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/callProfiles/' + id
    headers = {
        'Authorization': Authorization
    }

    res = requests.put(url, headers=headers, verify=False, data=callProfiles_data)

    return res


# from backend.djangoapps.common.api.views import api_callProfiles_Delete
def api_callProfiles_Delete(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/callProfiles/' + id
    r = requests.delete(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'

    return r


# from backend.djangoapps.common.api.views import api_activeCallLegs
def api_activeCallLegs(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/calls/{id}/callLegs'.format(id=id)
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    requestCnt = (int(resDataJson['callLegs']['@total']) / 10) + 1 \
        if (int(resDataJson['callLegs']['@total']) % 10) != 0 \
        else int(resDataJson['callLegs']['@total']) / 10

    resDataList = list()

    for n in range(0, int(requestCnt)):
        url = 'https://' + apiUrl + '/api/v1/calls/{id}/callLegs?offset={offset}&limit=10'.format(offset=n * 10, id=id)
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'UTF-8'
        res_data = str(res.text)
        res_o = xmltodict.parse(res_data)
        res_data = json.dumps(res_o)
        res_data_json = json.loads(res_data)
        if type(res_data_json['callLegs']['callLeg']) == list:
            resDataList.append(res_data_json['callLegs']['callLeg'])
        else:
            single_data = [res_data_json['callLegs']['callLeg']]
            resDataList.append(single_data)

    totDataList = list()
    for list_data in resDataList:
        for data in list_data:
            totDataList.append(data)

    return totDataList


# from backend.djangoapps.common.api.views import api_callProfiles_Id
def api_activeCallLegsId(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/calls/{id}/callLegs/'.format(id)
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_activeCallLegsId_POST
def api_activeCallLegsId_POST(id, user):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/calls/{id}/callLegs/'.format(id=id)
    headers = {
        'Authorization': Authorization
    }

    post_data = {"remoteParty": user}

    r = requests.post(url, headers=headers, verify=False, data=post_data)

    return r


# from backend.djangoapps.common.api.views import api_templateLegPro
def api_templateLegPro(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/callLegProfiles/' + id
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_templatePro
def api_templatePro(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/callProfiles/' + id
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_mornitoringStatus
def api_mornitoringStatus():
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/system/status'
    headers = {
        'Authorization': Authorization
    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_users
def api_users():
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/users'
    headers = {
        'Authorization': Authorization
    }

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    try:
        requestCnt = (int(resDataJson['users']['@total']) / 20) + 1
    except BaseException:
        requestCnt = 0

    resDataList = list()

    for n in range(0, int(requestCnt)):
        url = 'https://' + apiUrl + '/api/v1/users?offset={offset}&limit=20'.format(offset=n * 20)
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'UTF-8'
        res_data = str(res.text)
        res_o = xmltodict.parse(res_data)
        res_data = json.dumps(res_o)
        res_data_json = json.loads(res_data)
        resDataList.append(res_data_json['users']['user'])

    totDataList = list()
    for list_data in resDataList:
        for data in list_data:
            totDataList.append(data)

    return totDataList


# from backend.djangoapps.common.api.views import api_usersId
def api_usersId(id):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    headers = {
        'Authorization': Authorization,
    }

    url = 'https://' + apiUrl + '/api/v1/users/' + id

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


# from backend.djangoapps.common.api.views import api_cdrReceivers
def api_cdrReceivers():
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/system/cdrReceivers'
    headers = {
        'Authorization': Authorization
    }

    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8'
    resData = str(r.text)

    # xml to json
    o = xmltodict.parse(resData)
    resData = json.dumps(o)
    resDataJson = json.loads(resData)

    return resDataJson


def api_cdr_POST(request):
    json_data = json.dumps(request.POST)
    json_data = json.loads(json_data)

    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    url = 'https://' + apiUrl + '/api/v1/system/cdrReceivers'
    headers = {
        'Authorization': Authorization
    }

    r = requests.post(url, headers=headers, verify=False, data=json_data)

    return r


def api_cdr_PUT(request):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    id = request.POST.get('@id')

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/system/cdrReceivers/' + id
    headers = {
        'Authorization': Authorization
    }

    json_data = json.dumps(request.POST)
    json_data = json.loads(json_data)
    resDataJson = requests.put(url, headers=headers, verify=False, data=json_data)

    return resDataJson


def api_cdr_id(id, request=None):
    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    # requests GET
    url = 'https://' + apiUrl + '/api/v1/system/cdrReceivers/' + id
    headers = {
        'Authorization': Authorization
    }
    if request is not None:
        json_data = json.dumps(request.POST)
        json_data = json.loads(json_data)
        resDataJson = requests.put(url, headers=headers, verify=False, data=json_data)

    else:
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = 'UTF-8'
        resData = str(r.text)

        # xml to json
        o = xmltodict.parse(resData)
        resData = json.dumps(o)
        resDataJson = json.loads(resData)

    return resDataJson


def api_cdr_del(request):
    cdr_listID = request.POST.getlist('del_arr[]')

    Authorization = getAuthToken()
    apiUrl = getApiUrl()

    headers = {
        'Authorization': Authorization
    }
    error_id = list()
    for cdrId in cdr_listID:
        url = 'https://' + apiUrl + '/api/v1/system/cdrReceivers/' + cdrId
        r = requests.delete(url, headers=headers, verify=False)
        r.encoding = 'UTF-8'

        if r.status_code != 200:
            error_id.append(r)

    return error_id


def apiCheckCall(request):
    coSpaceId = request.POST.get("coSpace")
    Authorization = getAuthTokenBasic()
    apiUrl = getApiUrlBasic()

    headers = {
        'Authorization': Authorization
    }
    url = 'https://' + apiUrl + '/api/v1/calls?coSpaceFilter=' + coSpaceId
    r = requests.get(url, headers=headers, verify=False)
    r.encdoing = 'UTF-8'
    return r


def callApiId(url, jsonParam, type, start=None, server_seq=None):
    server_seq = server_seq
    try:
        api_json = coreJson()
        api_list = list()
        res = ""
        for idx, server in enumerate(api_json['api'], 1):
            Authorization = getAuthToken(server['userName'], server['password'])
            apiUrl = getApiUrl(server['ipAddress'], server['port'])
            useHttps = getUseHttps(server['useHttps'])

            fullurl = ""

            if useHttps is True:
                fullurl = "https://"
            else:
                fullurl = "http://"

            fullurl = fullurl + apiUrl + '/api/v1/' + url
            headers = {
                'Authorization': Authorization
            }
            if type == "GET":
                if server_seq is None:
                    res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                    res_json = api_status_data(res)
                    if res_json['status'] == 200:
                        # 한 서버의 모든 데이터를 가져오는 함수 실행
                        list_data = api_data_id_server(fullurl, start, url, headers, server['seq'])
                        api_list.extend(list_data)
                    if idx == len(api_json['api']):
                        # api_list = list(set(api_list))
                        retData = {'error': res_json['error'], 'body': api_list, 'status': res.status_code}
                        return retData

                    continue
                elif server_seq == server['seq']:
                    res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
                    res_json = api_status_data(res)
                    if res_json['status'] == 200:
                        # 한 서버의 모든 데이터를 가져오는 함수 실행
                        list_data = api_data_id_server(fullurl, start, url, headers, server_seq)
                        api_dict = dict()
                        retData = {'headers': headers, 'body': list_data, 'status': res.status_code}
                        return retData
                else:
                    continue
            elif type == "POST" and server['seq'] == server_seq:
                res = requests.post(fullurl, headers=headers, verify=False, data=jsonParam)
            elif type == "PUT" and server['seq'] == server_seq:
                res = requests.put(fullurl, headers=headers, verify=False, data=jsonParam)
            elif type == "DELETE" and server['seq'] == server_seq:
                res = requests.delete(fullurl, headers=headers, verify=False, data=jsonParam)

            retData = api_status_data(res, server['seq']) if res != '' else ''

    except BaseException as e:
        # log 파일에 에러 내용 추가 예정
        retData = dict()
        retData['status'] = 99999
        retData['error'] = '알 수 없는 에러가 발생하였습니다.'

        return retData

    return retData


# from backend.djangoapps.common.api.views import api_data_list serverside 통신
def api_data_id_server(url, start, data_key, headers, server_seq=None):
    offset = start
    res_list = list()
    if start != None:
        call_uri = url + '?offset={offset}&limit=10'.format(offset=offset)
    else:
        call_uri = url
    # api 직접 호출
    res_json = requests.get(call_uri, headers=headers, verify=False)
    retData = api_status_data(res_json, server_seq)
    if retData['status'] == 200:
        retData['body']['server_seq'] = server_seq
        res_list.append(retData['body'])
    return res_list


def apiCheckCall_copy(request):
    server_seq = request.POST.get("server_seq")
    coSpaceId = request.POST.get("coSpace")
    api_json = coreJson()
    res_list = list()
    res = ""
    for idx, server in enumerate(api_json['api'], 1):
        if server_seq == 'None':
            Authorization = getAuthToken(server['userName'], server['password'])
            apiUrl = getApiUrl(server['ipAddress'], server['port'])
            useHttps = getUseHttps(server['useHttps'])
            fullurl = ""

            if useHttps is True:
                fullurl = "https://"
            else:
                fullurl = "http://"

            fullurl = 'https://' + apiUrl + '/api/v1/calls?coSpaceFilter=' + coSpaceId
            headers = {
                'Authorization': Authorization
            }
            res = requests.get(fullurl, headers=headers, verify=False)
            res.encdoing = 'UTF-8'
            res_list.append(res)
        else:
            if server_seq == server['seq']:
                Authorization = getAuthToken(server['userName'], server['password'])
                apiUrl = getApiUrl(server['ipAddress'], server['port'])
                useHttps = getUseHttps(server['useHttps'])
                fullurl = ""

                if useHttps is True:
                    fullurl = "https://"
                else:
                    fullurl = "http://"

                fullurl = 'https://' + apiUrl + '/api/v1/calls?coSpaceFilter=' + coSpaceId
                headers = {
                    'Authorization': Authorization
                }
                res = requests.get(fullurl, headers=headers, verify=False)
                res.encdoing = 'UTF-8'
                res_list.append(res)
    return res_list


def api_activeCallId_add_copy(request):
    json_data = json.dumps(request.POST)
    json_data = json.loads(json_data)
    server_seq = request.POST['server_seq']
    api_json = coreJson()
    res_list = list()
    res = ""
    for idx, server in enumerate(api_json['api'], 1):
        if server_seq == 'None':
            Authorization = getAuthToken(server['userName'], server['password'])
            apiUrl = getApiUrl(server['ipAddress'], server['port'])
            useHttps = getUseHttps(server['useHttps'])
            fullurl = ""

            if useHttps is True:
                fullurl = "https://"
            else:
                fullurl = "http://"

            fullurl = 'https://' + apiUrl + '/api/v1/calls'
            headers = {
                'Authorization': Authorization
            }
            # if server_seq == server['seq']:
            res = requests.post(fullurl, headers=headers, verify=False, data=json_data)
            res.encdoing = 'UTF-8'
            res_list.append(res)
        else:
            if server_seq == server['seq']:
                Authorization = getAuthToken(server['userName'], server['password'])
                apiUrl = getApiUrl(server['ipAddress'], server['port'])
                useHttps = getUseHttps(server['useHttps'])
                fullurl = ""

                if useHttps is True:
                    fullurl = "https://"
                else:
                    fullurl = "http://"

                fullurl = 'https://' + apiUrl + '/api/v1/calls'
                headers = {
                    'Authorization': Authorization
                }
                # if server_seq == server['seq']:
                res = requests.post(fullurl, headers=headers, verify=False, data=json_data)
                res.encdoing = 'UTF-8'
                res_list.append(res)

    return res_list


def call_total(url, jsonParam, type):
    api_json = coreJson()
    api_list = list()
    total_list = list()
    res = ""
    for idx, server in enumerate(api_json['api'], 1):
        Authorization = getAuthToken(server['userName'], server['password'])
        apiUrl = getApiUrl(server['ipAddress'], server['port'])
        useHttps = getUseHttps(server['useHttps'])

        fullurl = ""

        if useHttps is True:
            fullurl = "https://"
        else:
            fullurl = "http://"

        fullurl = fullurl + apiUrl + '/api/v1/' + url
        headers = {
            'Authorization': Authorization
        }
        res = requests.get(fullurl, headers=headers, verify=False, data=jsonParam)
        res_json = api_status_data(res)
        if int(res_json['status']) == 200:
            total = int(res_json['body'][url]['@total'])
            total_list.append(total)
        else:
            total = 0
            total_list.append(total)
    for i in range(0, len(total_list)):
        if total_list[0] <= total_list[i]:
            total_list[0] = total_list[i]
    return int(total_list[0])
