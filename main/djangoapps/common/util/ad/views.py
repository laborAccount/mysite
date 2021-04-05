#-*- coding: utf-8 -*-
import string
import random
import requests
import json

from django.db import connections
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from backend.djangoapps.common.com.views import CiscoApi

class AdApi:
    
    def db_create(self,user_tel,user_id=None):
        #DB 조회 및 아이디 생성
        string_len = 3
        int_len = 4

        ran_str = string.ascii_lowercase
        ran_int = string.digits

        pwdstr = ""
        idstr = ""

        for i in range(string_len):
            pwdstr += random.choice(ran_str)

        for j in range(int_len):
            pwdstr += random.choice(ran_int)

        user_pwd = pwdstr + "!"

        if user_id is not None:
            idstr = user_id
        else :
            idstr = 'anonymous'

        with connections['default'].cursor() as cur:
            query = '''
                SELECT
                    IFNULL(LPAD(MAX(RIGHT(SUBSTRING_INDEX(user_id,'@',1),2))+1 ,2,0),'01')
                FROM kt_ad_user_list
                WHERE add_id = '{user_id}'
                AND del_yn ='N'
            '''.format(user_id=idstr)
            cur.execute(query)
            row = cur.fetchone()
            cur.close()
            intstr = row[0]

        user_id = idstr+intstr
        context = dict()
        context['user_id'] = user_id
        context['user_pwd'] = user_pwd
        context['user_tel'] = user_tel
        context['idstr'] = idstr

        return context

    def ad_create(self,user_id,user_pwd,user_tel):
        jsonParam = dict()
        jsonParam['user_id'] = user_id
        jsonParam['user_pwd'] = user_pwd

        jsonDump = json.dumps(jsonParam)
        #ad requet
        f = open(settings.EXTEND_KT_AD, 'r')
        rawData = f.read()
        f.close()
        jsonData = json.loads(rawData)
        baseurl = jsonData['AD_API_URL']

        fullurl = baseurl+"/add"
        headers = dict()
        headers['Content-Type'] = "application/json"

        res = requests.post(fullurl, headers=headers, verify=False, json=jsonParam)

        ret = json.loads(res.text)
        retData = {}
        retData['result'] = ret['result']
        retData['user_id'] = user_id
        retData['user_pwd'] = user_pwd
        retData['user_tel'] = user_tel
        return retData

    def db_delete(self,user_id,session_id):
        try:
            #delete_yn 변경
            with connections['default'].cursor() as cur:
                query = '''
                    UPDATE kt_ad_user_list
                    SET
                        del_yn = 'Y',
                        use_yn = 'N',
                        del_date = NOW(),
                        del_id = '{session_id}'
                    WHERE
                        user_id = '{user_id}'
                        and del_yn = 'N'
                '''.format(user_id=user_id,session_id=session_id)
                cur.execute(query)
            result='success'
        except:
            result="false"
        return result

    def ad_delete(self,user_id):
        f = open(settings.EXTEND_KT_AD, 'r')
        rawData = f.read()
        f.close()
        jsonData = json.loads(rawData)
        baseurl = jsonData['AD_API_URL']

        fullurl = baseurl+"/remove"
        headers = dict()
        headers['Content-Type'] = "application/json"
        jsonParam = dict()
        jsonParam['user_id'] = user_id

        res = requests.post(fullurl, headers=headers, verify=False, json=jsonParam)
        ret = json.loads(res.text)
        retData = {}
        retData['result'] = ret['result']
        retData['user_id'] = user_id
        ca = CiscoApi()
        ca.setServerSeqData(1)
        api_data = ca.comCallAPI('ldapSyncs', 'POST')
        return retData

    def id_init(self,user_id,session_id):
        try:
            with connections['default'].cursor() as cur:
                query = '''
                    UPDATE kt_ad_user_list
                    SET
                        del_yn = 'Y',
                        use_yn = 'N',
                        del_id = '{del_id}'
                    WHERE
                        user_id = '{user_id}'
                '''.format(user_id=user_id,del_id=session_id)
                cur.execute(query)
            result='success'
        except:
            result='false'
        return result

    def ldap_sync(self):

        result = "success"
        ca = CiscoApi()
        ca.setServerSeqData(1)
        api_data = ca.comCallAPI('ldapSyncs', 'POST')

        return result

def ad_id_init(request):
    json_data = json.loads(request.POST.get('data'))
    session_id = request.session['user_id']
    ad_id_arr = json_data['ad_id_arr']
    ad = AdApi()
    ret = 'false'
    for i in range(0,len(ad_id_arr)):
        ret = ad.id_init(ad_id_arr[i],session_id)
    return JsonResponse({"result":ret})

def create_ad(request):
    json_data = json.loads(request.POST.get('data'))
    call_id = request.POST.get('call_id')
    cospace_id = request.POST.get('cospace_id')
    ad_id_arr = json_data['ad_id_arr']
    ad = AdApi()
    ret = list()
    result = 'false'
    for ad_data in ad_id_arr:
        retData = ad.ad_create(ad_data['user_id'],ad_data['user_pwd'],ad_data['user_tel'])
        ret.append(retData)
        if retData['result'] == 'success':
            # db update
            with connections['default'].cursor() as cur:
                query = '''
                    UPDATE kt_ad_user_list
                    SET cospace_guid = '{cospace_id}', call_guid = '{call_id}'
                    WHERE user_id = '{user_id}'
                '''.format(user_id=ad_data['user_id'],cospace_id=cospace_id,call_id=call_id)
                cur.execute(query)
        #ldap sync
        ad.ldap_sync()
    for i in range(0,len(ret)):
        if ret[i]['result'] == 'success' :
            result = 'success'
    return JsonResponse({"result":result})




def delete_ad(request):
    user_id = request.POST.get("data")
    session_id = request.session['user_id']
    ad = AdApi()
    ret1 = ad.db_delete(user_id,session_id)
    ret2 = ad.ad_delete(user_id)
    result = 'success'
    if ret1 == 'false' and ret2 =='false':
        result = 'false'
    return JsonResponse({"result":result})
