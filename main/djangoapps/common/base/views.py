# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db import connections
from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.http import HttpResponse, JsonResponse

from datetime import datetime

# api.json
from backend.djangoapps.common.core.views import coreJson
from backend.djangoapps.common.core.views import api_coreJson

from django.contrib import auth

import json
import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES
from main.settings import SECRET_KEY

# hashed_password = property(get_password, set_password)
# print(str(hashlib.sha256('asdfasdfasdfasdf'.encode('utf-8')).hexdigest()))
# print(str(hashlib.sha256('avav'.encode('utf-8')).hexdigest()))

class AESCipher:
    def __init__(self):
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-s[-1]]
        self.key = hashlib.sha256(SECRET_KEY.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = self.pad(raw).encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))

    def encrypt_str(self, raw):
        return self.encrypt(raw).decode('utf-8')

    def decrypt_str(self, enc):
        if type(enc) == str:
            enc = str.encode(enc)
        return self.decrypt(enc).decode('utf-8')


'''
Author  : syh
Desc    : 로그인 페이지 로드 및 로그인
History
2019.06.11 최초작성
2019.12.17 password 수정(Author  : JHY)
'''
def password_sha(passwd=None):
    passwd = str(hashlib.sha256(passwd.encode('utf-8')).hexdigest())
    return passwd

def login(request):
    context = dict()
    if "user_id" in dict(request.session):
        return redirect('/main')
    return render(request, 'common/base/login.html', context)


def login_ajax(request):
    context = dict()
    inputId = request.POST.get('inputId')
    inputPw = request.POST.get('inputPw')
    # print('-------------',inputPw)

    if inputId == '' and inputPw == '':
        context['result'] = 'valid'
        return JsonResponse(context)
#    try:
    # with connections['default'].cursor() as cur:
    #     query = '''
    #             select user_pwd
    #             from cms_manager
    #             where user_id = '{user_id}'
    #     '''.format(user_id=inputId)
    #     cur.execute(query)
    #     u_pwd = cur.fetchall()
    #     cur.close()
    #
    #     real_pwd = u_pwd[0][0]

    with connections['default'].cursor() as cur:
        query = '''
                SELECT
                    a.user_id,
                    a.user_name,
                    a.user_role,
                    a.language,
                    b.add_param1 as `level`,
                    a.user_pwd
                FROM cms_manager a
                INNER JOIN cms_code_detail b
                    ON b.group_code = '001'
                    AND b.detail_code = a.user_role
                WHERE a.user_id = '{user_id}'
        '''.format(user_id=inputId)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

    if len(rows) > 0 :
        if rows[0][5] == password_sha(inputPw):
            request.session['user_id'] = rows[0][0]
            request.session['user_name'] = rows[0][1]
            request.session['language'] = rows[0][3]
            request.session['user_role'] = rows[0][2]
            request.session['user_level'] = rows[0][4]
            request.session[translation.LANGUAGE_SESSION_KEY] = rows[0][3]
            translation.activate(rows[0][3])

            user_id = request.session['user_id']
            login_ip = get_client_ip(request)
            login_date = datetime.now()
            login_status = 'Success'
            with connections['default'].cursor() as cur:
                query = '''
                    INSERT INTO cms_login_log(user_id,login_ip,login_status,login_date)
                    VALUES ('{user_id}','{login_ip}','{login_status}','{login_date}')
                '''.format(user_id=user_id, login_ip=login_ip, login_status=login_status, login_date=login_date)
                cur.execute(query)
            return JsonResponse({'result': 'success'})
        else :
            context['result'] = 'valid'
            return JsonResponse(context)

    else:  # 로그인 실패
        user_id = inputId
        login_ip = get_client_ip(request)
        login_date = datetime.now()
        login_status = 'Failed'
        with connections['default'].cursor() as cur:
            query = '''
                INSERT INTO cms_login_log(user_id,login_ip,login_status,login_date)
                VALUES ('{user_id}','{login_ip}','{login_status}','{login_date}')
            '''.format(user_id=user_id, login_ip=login_ip, login_status=login_status, login_date=login_date)
            cur.execute(query)
        context['result'] = 'valid'
        return JsonResponse(context)

#    except Exception as be:
#        print(be)
#        context['result'] = 'server_err'
#        return JsonResponse(context)


'''
Author  : syh
Desc    : 공통 좌측 메뉴
History
2019.06.11 최초작성
'''


def main_side_bar(request):
    user_id = request.session['user_id']
    user_role = request.session['user_role']

    with connections['default'].cursor() as cur:
        query = '''
                SELECT
                    d.code_name,
                    a.menu_seq,
                    a.menu_name,
                    b.user_role,
                    a.menu_url,
                    MAX(d.add_param2) AS add_param2,
                    a.up_menu_seq
                FROM cms_menu a
                JOIN cms_code_detail d ON d.group_code = '003' and a.up_menu_seq = d.detail_code
                JOIN cms_manager_menu c ON c.menu_seq = a.menu_seq
                JOIN cms_manager b  ON b.user_id = c.user_id
                INNER JOIN cms_menu_default e ON e.user_role = b.user_role AND e.menu_seq = c.menu_seq AND e.default_yn = 'Y'
                WHERE b.user_role = '{user_role}' AND b.user_id ='{user_id}' AND a.delete_yn='N' AND e.default_yn = 'Y'
                GROUP BY menu_seq
                ORDER BY menu_seq
        '''.format(user_role=user_role, user_id=user_id)
        cur.execute(query)
        rows = cur.fetchall()

        menu_list = []
        check = 'xxx'
        for row in rows:
            dict = {}
            if check != row[0]:
                dict['menu'] = row[0]
                dict['menu_class'] = row[5]
                dict['submenu'] = []

                if row[6] == row[1]:
                    dict['menu_url'] = row[4]
                menu_list.append(dict)
                check = row[0]
        for item in menu_list:
            for row in rows:
                if item['menu'] == row[0]:
                    if row[6] != row[1]:
                        item['submenu'].append([row[4], row[2]])
    context = {}
    context['menu_list'] = menu_list
    return JsonResponse({'return': context})


'''
Author  : kkm
Desc    : 사용자 IP 정보
History
2019.06.11 최초작성
'''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def settings(request):
    coreData = coreJson()
    api_coreData = api_coreJson()
    

    # return HttpResponse({"var test_api_json = "+json.dumps(coreData)},{"var _api_json = " + json.dumps(api_coreData)})
    return HttpResponse("var _api_json = " + json.dumps(coreData) + "; var _test_api_json = " + json.dumps(api_coreData))


'''
Author  : syh
Desc    : 로그아웃
History
2019.08.19 최초작성
'''


def logout(request):
    auth.logout(request)

    del request.session

    return HttpResponse("/")


'''
Author  : syh
Desc    : 비밀번호 변경
History
2019.08.19 최초작성
2019.12.17 수정 (JHY)
'''


def change_password(request):
    retJson = {}

    session_user_id = request.session["user_id"]
    bPassword = request.POST.get("bPassword")
    aPassword = request.POST.get("aPassword")
    cPassword = request.POST.get("cPassword")

    if (aPassword != cPassword):
        return JsonResponse({'result': 'error'})

    sha_password = password_sha(cPassword)

    modify_date = datetime.now()
    with connections['default'].cursor() as sCur:
        sQuery = '''
                SELECT
                    user_pwd
                FROM cms_manager
                WHERE
                    user_id = '{user_id}'
        '''.format(user_id=session_user_id)
        sCur.execute(sQuery)
        user_pwd = sCur.fetchall()
        if user_pwd[0][0] != password_sha(bPassword):
            retJson = {"result": "fail"}

        elif len(user_pwd[0][0]) == 0:
            retJson = {"result": "fail"}

        else:

            try:
                with connections['default'].cursor() as uCur:
                    uQuery = '''
                            UPDATE cms_manager SET
                                user_pwd = '{user_pwd}'
                                , pw_change_date = '{modify_date}'
                                , modify_id = '{user_id}'
                                , modify_date = '{modify_date}'
                            WHERE
                                user_id = '{user_id}'
                    '''.format(user_id=session_user_id, user_pwd=sha_password, modify_date=modify_date)
                    uCur.execute(uQuery)
                retJson = {"result": "success"}

            except BaseException as be:
                print(be)
                return JsonResponse({'result': 'error'})

    return JsonResponse(retJson)


'''
Author  : syh
Desc    : 언어 변경
History
2019.08.19 최초작성
'''


def transLang(request):
    userLanguage = request.POST.get('lang')

    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    translation.activate(userLanguage)
    request.session[translation.LANGUAGE_SESSION_KEY] = userLanguage

    return JsonResponse({'return': 'success'})
