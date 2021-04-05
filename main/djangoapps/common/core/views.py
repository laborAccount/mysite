#-*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.conf import settings

#UTIL
import json
import requests
import xmltodict
#import pybase64


#from backend.djangoapps.common.core.views import getAuthToken
def getAuthTokenBasic():

    jsonData = coreJson()

    id = jsonData['api'][0]['userName']
    pw = jsonData['api'][0]['password']

    rawData = id + ':' + pw
    encData = pybase64.b64encode(rawData.encode(), altchars='_:')
    auth = 'Basic ' + encData.decode()

    return auth

def getAuthToken(id, pw):

    # jsonData = coreJson()
    #
    # id = jsonData['api'][0]['userName']
    # pw = jsonData['api'][0]['password']

    rawData = id + ':' + pw
    encData = pybase64.b64encode(rawData.encode(), altchars='_:')
    auth = 'Basic ' + encData.decode()

    return auth

def getApiUrlBasic():
    jsonData = coreJson()

    url = jsonData['api'][0]['ipAddress']
    port = jsonData['api'][0]['port']

    fullUrl = url+":"+port

    return fullUrl

def getApiUrl(url, port):
    # jsonData = coreJson()
    #
    # url = jsonData['api'][0]['ipAddress']
    # port = jsonData['api'][0]['port']

    fullUrl = url+":"+port

    return fullUrl

def getUseHttpsBasic():
    jsonData = coreJson()

    useHttps = jsonData['api'][0]['useHttps']

    if useHttps == 'True' or useHttps is True or useHttps == 'true':
        return True
    else:
        return False

def getUseHttps(useHttps):
    # jsonData = coreJson()
    #
    # useHttps = jsonData['api'][0]['useHttps']

    if useHttps == 'True' or useHttps is True or useHttps == 'true':
        return True
    else:
        return False


def getErrorJson():
    f = open(settings.CORE_ERRORJSON_PATH, 'r')
    rawData = f.read()
    f.close()
    jsonData = json.loads(rawData)

    return jsonData


'''
Author  : kkm
Desc    : api.json 리턴
History
2019.06.11 최초작성
2020.01.07 timeout_cnt 추가(jhy)
'''
def coreJson():
    f = open(settings.CORE_APIJSON_PATH, 'r', encoding='UTF-8-sig')
    rawData = f.read()
    f.close()
    jsonData = json.loads(rawData)

    return jsonData

def timout_cnt_Json():
    f = open(settings.CORE_TIMEOUT_CNT_PATH, 'r', encoding='UTF-8-sig')
    rawData = f.read()
    f.close()
    jsonData = json.loads(rawData)

    return jsonData

#from backend.djangoapps.common.api.views import api_command
@csrf_exempt
def ccChange(request):

    mode = request.POST.get('mode') # txVideoMute
    flag = request.POST.get('flag') # on

    f = open(settings.CORE_APIJSON_PATH, 'r')
    rawData = f.read()
    f.close()
    jsonData = json.loads(rawData)

    if mode == 'txVideoMute':
        if flag == 'on':
            jsonData['callcommand']['txVideoMute'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['txVideoMute'] = 'false'
    elif mode == 'videoMode':
        if flag == 'on':
            jsonData['callcommand']['videoMode'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['videoMode'] = 'false'
    elif mode == 'txAudioMute':
        if flag == 'on':
            jsonData['callcommand']['txAudioMute'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['txAudioMute'] = 'false'
    elif mode == 'rxAudioMute':
        if flag == 'on':
            jsonData['callcommand']['rxAudioMute'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['rxAudioMute'] = 'false'
    elif mode == 'presentationContributionAllowed':
        if flag == 'on':
            jsonData['callcommand']['presentationContributionAllowed'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['presentationContributionAllowed'] = 'false'
    elif mode == 'presentationViewingAllowed':
        if flag == 'on':
            jsonData['callcommand']['presentationViewingAllowed'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['presentationViewingAllowed'] = 'false'
    elif mode == 'rxVideoMute':
        if flag == 'on':
            jsonData['callcommand']['rxVideoMute'] = 'true'
        elif flag == 'off':
            jsonData['callcommand']['rxVideoMute'] = 'false'

    rawData = json.dumps(jsonData)

    f = open(settings.CORE_APIJSON_PATH, 'w')
    f.write(rawData)
    f.close()

    return JsonResponse({'return':'success'})

def api_coreJson():
    f = open(settings.CORE_TESTAPIJSON_PATH, 'r', encoding='UTF-8-sig')
    rawData = f.read()
    f.close()
    jsonData = json.loads(rawData)

    return jsonData
