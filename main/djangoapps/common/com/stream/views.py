#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.conf import settings
import logging
import logging.config
#UTIL
import json
import requests
import urllib3
import pybase64
import xmltodict
from urllib3.exceptions import HTTPError
import asyncio
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class StreamApi:

    def __init__(self):                     # 초기 셋팅 기본값으로 api.json 의 0번 리스트 값을 입력

        self.url = None
        self.res_headers = None             # Response Header 정보
        self.res_body = None                # Response Body 데이터
        self.retData = None
        self.total = None                   # API 결과값중 Total 이 있을경우 Total 값
        self.error = None                   # API 호출시 에러에 대한 정보 , 내용을 입력해둘것
        self.query_string = None            # API GET 호출시 Query Param 에 대한 스트링 조합값
        self.status = None                  # Response Status 코드값
        # self.full_url = 'http://demo.weandsoft.com/'                 # 실제 API 호출할 Full Url
        self.full_url = 'http://121.140.142.233/'                 # 실제 API 호출할 Full Url


    def comStreamAPI(self, url, type, query_param = None, jsonParam = None ):

        self.url = url
        self.status = None
        self.res_headers = None
        self.res_body = None
        self.error = None
        self.total = None
        self.retData = {}
        self.retData['status'] = None
        self.retData['headers'] = None
        self.retData['body'] = None
        self.retData['error'] = None
        self.retData['total'] = 0

        self.full_url = self.full_url+self.url

        try :
            if 'GET' == type :
                if query_param is not None :
                    if isinstance(query_param,dict) :
                        tempCount = 0
                        for key, value in query_param.items() :
                            if 0 == tempCount :
                                self.query_string = "?"+str(key)+"="+str(value)
                            else :
                                self.query_string = self.query_string+"&"+str(key)+"="+str(value)
                            tempCount = tempCount+1
                    self.full_url = self.full_url + self.query_string
                res = requests.get(self.full_url, data=jsonParam)

            # elif 'POST' == type :
            #     res = requests.post(self.full_url, headers=self.req_headers, verify=False, data=jsonParam)
            # elif 'PUT' == type :
            #     res = requests.put(self.full_url, headers=self.req_headers, verify=False, data=jsonParam)
            # elif 'DELETE' == type :
            #     res = requests.delete(self.full_url, headers=self.req_headers, verify=False, data=jsonParam)
            res.encoding = 'UTF-8'

        except requests.Timeout as timeoutEx:
            self.retData['error'] = 'NetworkConnection TimeOut'
        except BaseException as baseEx:
            self.retData['error'] = 'Unknown Exception'
        else:
            self.status = int(res.status_code)
            if 200 == self.status :
                self.res_headers = res.headers
                if type == 'GET' :
                    self.res_body = self.api_data_to_json(res.text)
                    for key, value in self.res_body.items() :
                        if 'totalCount' in self.res_body[key] :
                            self.total = int(self.res_body[key]['totalCount'])
                        else :
                            self.total = None

            elif 400 == self.status :
                self.error = self.api_get_error_message(res.text)
            elif 401 == self.status :
                self.error = '401 Unauthorized'
            elif 404 == self.status :
                self.error = '404 Not Found'
            else :
                self.error = "Unknown Error"

            self.retData['status'] = self.status
            self.retData['headers'] = self.res_headers
            self.retData['body'] = self.res_body
            self.retData['error'] = self.error
            self.retData['total'] = self.total

        finally:
            return self.retData

    def api_data_to_json(self,res_txt):
        try :
            if res_txt is not '':

                o = xmltodict.parse(res_txt)
                res_data = json.dumps(o)
                res_json = json.loads(res_data)
                return res_json

        except BaseException as baseEx :
            return {}

    def showData(self):
        pass
