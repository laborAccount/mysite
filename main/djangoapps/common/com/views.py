# -*- coding: utf-8 -*-
from django.conf import settings
# import logging
# import logging.config
# UTIL
import json
import requests
import urllib3
import pybase64
import xmltodict
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# api 전체 서버 정보
from main.djangoapps.common.core.views import coreJson

import traceback
import logging

# 전역 변수
logger = logging.getLogger('sys')

'''
Author  : kkm
Desc    : 공통 API
History
2019.06.11 최초작성
'''


class CiscoApi:

    def __init__(self):  # 초기 셋팅 기본값으로 api.json 의 0번 리스트 값을 입력

        self.ip_address = None  # CMS IP
        self.port = None  # CMS PORT
        self.url = None  # API URL
        self.use_https = None  # HTTP 사용여부
        self.admin_id = None  # CMS ADMIN ID
        self.admin_pw = None  # CMS ADMIN PASSWORD
        self.req_headers = None  # Request Header 정보
        self.res_headers = None  # Response Header 정보
        self.res_body = None  # Response Body 데이터
        self.retData = None
        self.total = None  # API 결과값중 Total 이 있을경우 Total 값
        self.error = None  # API 호출시 에러에 대한 정보 , 내용을 입력해둘것
        self.query_string = None  # API GET 호출시 Query Param 에 대한 스트링 조합값
        self.param = None  # API POST, PUT Parameter
        self.status = None  # Response Status 코드값
        self.server_seq = None  # API 호출한 Server_seq  (api.json 데이터)
        self.server_name = None  # API 호출한 Server_name (api.json 데이터)
        self.full_url = None  # 실제 API 호출할 Full Url
        self.group_seq = None
        self.group_name = None

        self.setServerSeqData(0)

    def createAuthTokenBasic(self):  # ID 와 Password로 Headers Authorization 을 생성

        rawData = self.admin_id + ':' + self.admin_pw
        encData = pybase64.b64encode(rawData.encode(), altchars='_:')
        auth = 'Basic ' + encData.decode()
        self.req_headers = {
            'Authorization': auth
        }

    def setGroupSeqData(self, group_data):
        self.group_seq = group_data['group_seq']
        self.group_name = str(group_data['group_name'])

    def setGroupSeq(self, group_seq):
        if type(group_seq) != type(str()):
            self.group_seq = str(group_seq)
        else:
            self.group_seq = group_seq

        jsonData = coreJson()
        for data in jsonData['api']:
            if self.group_seq == data['group_seq']:
                self.group_name = str(data['group_name'])

    def setServerSeqData(self, server_seq):
        group_data = dict()
        jsonData = coreJson()
        for data in jsonData['api']:
            if data['group_seq'] == str(self.group_seq):
                group_data['api'] = data['api_list']
                self.setServerData(group_data['api'][int(server_seq)])
                break

    def setServerData(self, server_info):  # 서버 정보를 설정
        self.ip_address = server_info['ipAddress']
        self.port = server_info['port']
        self.use_https = server_info['useHttps']
        self.admin_id = server_info['userName']
        self.admin_pw = server_info['password']
        self.server_seq = server_info['seq']
        self.server_name = server_info['serverName']
        self.createAuthTokenBasic()

    def comCallAPI(self, url, type, query_param=None, headers=None, jsonParam=None, timeout=None):
        self.default_timeout = 1
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
        self.retData['server_seq'] = self.server_seq
        self.retData['server_name'] = self.server_name

        if headers is not None:
            self.req_headers.update(headers)

        if self.use_https == True or self.use_https == 'True' or self.use_https == 'true':
            self.full_url = 'https://'
        else:
            self.full_url = 'http://'

        self.full_url = self.full_url + self.ip_address + ':' + self.port + '/api/v1/' + self.url

        if timeout is not None:
            self.default_timeout = timeout

        try:
            # startT = datetime.datetime.now()
            if 'GET' == type:
                if query_param is not None:
                    if isinstance(query_param, dict):
                        tempCount = 0
                        for key, value in query_param.items():
                            if 0 == tempCount:
                                self.query_string = "?" + str(key) + "=" + str(value)
                            else:
                                self.query_string = self.query_string + "&" + str(key) + "=" + str(value)
                            tempCount = tempCount + 1
                    self.full_url = self.full_url + self.query_string
                res = requests.get(self.full_url, headers=self.req_headers, verify=False, data=jsonParam,
                                   timeout=self.default_timeout)
            elif 'POST' == type:
                res = requests.post(self.full_url, headers=self.req_headers, verify=False, data=jsonParam,
                                    timeout=self.default_timeout)
            elif 'PUT' == type:
                res = requests.put(self.full_url, headers=self.req_headers, verify=False, data=jsonParam,
                                   timeout=self.default_timeout)
            elif 'DELETE' == type:
                res = requests.delete(self.full_url, headers=self.req_headers, verify=False, data=jsonParam,
                                      timeout=self.default_timeout)
            # endT = datetime.datetime.now()
            # print("RTT : ",endT-startT)
            res.encoding = 'UTF-8'

        except requests.ConnectionError as ce:
            self.retData['error'] = 'ConnectionError'
            logger.error(ce)
        except requests.HTTPError as he:
            self.retData['error'] = 'HTTPError'
            logger.error(he)
        except requests.URLRequired as ur:
            self.retData['error'] = 'URLRequired'
            logger.error(ur)
        except requests.TooManyRedirects as tmr:
            self.retData['error'] = 'TooManyRedirects'
            logger.error(tmr)
        except requests.ConnectTimeout as ct:
            self.retData['error'] = 'ConnectTimeout'
            logger.error(ct)
        except requests.ReadTimeout as rt:
            self.retData['error'] = 'ReadTimeout'
            logger.error(rt)
        except requests.Timeout as to:
            self.retData['error'] = 'Timeout'
            logger.error(to)
        except requests.RequestException as re:
            self.retData['error'] = 'RequestException'
            logger.error(re)
        except BaseException as baseEx:
            print('comCallAPI')
            logger.error(baseEx)
            self.retData['error'] = 'UnknownException'
        else:
            self.status = int(res.status_code)
            if 200 == self.status:
                self.res_headers = res.headers
                if type == 'GET':
                    self.res_body = self.api_data_to_json(res.text)
                    for key, value in self.res_body.items():
                        if '@total' in self.res_body[key]:
                            self.total = int(self.res_body[key]['@total'])
                        else:
                            self.total = None

            elif 400 == self.status:
                self.error = self.api_get_error_message(res.text)
            elif 401 == self.status:
                self.error = '401 Unauthorized'
            elif 404 == self.status:
                self.error = '404 Not Found'
            else:
                self.error = "Unknown Error"

            self.retData['status'] = self.status
            self.retData['headers'] = self.res_headers
            self.retData['body'] = self.res_body
            self.retData['error'] = self.error
            self.retData['total'] = self.total
            self.retData['group_seq'] = self.group_seq
            self.retData['group_name'] = self.group_name

        finally:
            return self.retData

    def api_data_to_json(self, res_txt):
        try:
            if res_txt is not '':
                o = xmltodict.parse(res_txt)
                res_data = json.dumps(o)
                res_json = json.loads(res_data)
                for key in res_json:
                    for key2 in res_json[key]:
                        if type(res_json[key][key2]) is dict:
                            temp_list = list()
                            temp_list.append(res_json[key][key2])
                            res_json[key][key2] = temp_list
                return res_json

        except BaseException as baseEx:
            print('api_data_to_json')

            try:
                # json parsing
                res_json = json.loads(res_txt)
                if 'templates' in res_json:
                    return res_json
                else:
                    return {}
            except:
                return {}

    def api_get_error_message(self, res_txt):  # Api Error Message 정리후 메시지 전송

        f = open(settings.CORE_ERRORJSON_PATH, 'r')
        rawData = f.read()
        f.close()
        defKeyJson = json.loads(rawData)
        defKeys = defKeyJson['failureDetails'].keys()

        o = xmltodict.parse(res_txt)
        errorData = json.dumps(o)
        errorJson = json.loads(errorData)

        errorKeys = list(errorJson['failureDetails'].keys())

        if errorKeys[0] in defKeys:
            return errorKeys[0]

    def showData(self):

        print("self.port : ", self.port)
        print("self.url : ", self.url)
        print("self.use_https : ", self.use_https)
        print("self.admin_id : ", self.admin_id)
        print("self.admin_pw : ", self.admin_pw)
        print("self.retData : ", self.retData)
        print("self.req_headers : ", self.req_headers)
        print("self.res_headers : ", self.res_headers)
        print("self.res_body : ", self.res_body)
        print("self.total : ", self.total)
        print("self.error : ", self.error)
        print("self.param : ", self.param)
        print("self.status : ", self.status)
        print("self.group_seq : ", self.group_seq)
        print("self.server_seq : ", self.server_seq)

    def get_server_data(self, group_seq, server_seq):
        result = ''
        api_list = coreJson()
        for group_list in api_list['api']:
            if group_list['group_seq'] == str(group_seq):
                for group_data in group_list['api_list']:
                    if group_data['seq'] == str(server_seq):
                        result = group_data
        return result

    def get_group_data(self, group_seq):
        result = ''
        api_list = coreJson()
        for group_list in api_list['api']:
            if group_list['group_seq'] == str(group_seq):
                result = group_list
        return result

    def get_authToken(self):
        url = ''
        try:
            if self.use_https == True or self.use_https == 'True' or self.use_https == 'true':
                self.full_url = 'https://'
            else:
                self.full_url = 'http://'

            self.full_url = self.full_url + self.ip_address + ':' + self.port + '/api/v1/authTokens'
            res = requests.post(self.full_url, headers=self.req_headers, verify=False)
            auth_token = res.headers['X-Cisco-CMS-Auth-Token']
            url = '/events/v1?authToken=' + auth_token
        except:
            print('token error')
        return url

    def get_coSpace_id(self, call_id):
        check_flag = True
        coSpace_id = ''
        api_list = coreJson()['api']
        for group_list in api_list:
            self.setGroupSeqData(group_list['group_seq'])
            for group_data in group_list['api_list']:
                self.setServerSeqData(group_data['seq'])
                api_data = self.comCallAPI('calls/{call_id}'.format(call_id=call_id), 'GET')
                if api_data['status'] == 200:
                    check_flag = False
                    coSpace_id = api_data['body']['ca∂ll']['coSpace']
        return coSpace_id

    def getSeqData(self):
        temp_dict = dict()
        temp_dict['group_seq'] = self.group_seq
        temp_dict['server_seq'] = self.server_seq
        return temp_dict
