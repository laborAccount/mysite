#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connections
from django.db.models import Count, Sum, Case, When
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict

#공통 API
from main.djangoapps.common.com.views import CiscoApi
from main.djangoapps.common.core.views import coreJson

#UTIL
import json
import asyncio
from datetime import date, datetime, timedelta
from django.utils import translation

import time

#MODEL
from main.models import ApiCdrCall
from main.djangoapps.common.util import views as TMUtility

import traceback
import logging

logger = logging.getLogger('sys')

'''
Author  : kkm
Desc    : 메인 페이지 로드
History
2019.06.11 최초작성
'''
def main(request):
    context = dict()

    try:
        request.session[translation.LANGUAGE_SESSION_KEY]
        request.session['user_role']
        request.session['user_name']
    except BaseException as e:
        return render(request, 'common/base/login.html')

    return render(request, 'main/main.html', context)

def main_read(request):
    context = dict()
    static_list = list()

    try:
        statistics_query = '''
            WITH t AS (
                SELECT DATE_FORMAT(curdate(),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 2 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 3 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 4 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 5 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 6 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 7 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 8 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 9 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 10 MONTH),'%Y-%m') AS 'ym'
                UNION ALL
                SELECT DATE_FORMAT(DATE_SUB(curdate(), INTERVAL 11 MONTH),'%Y-%m') AS 'ym'
            )
            SELECT 
                t.ym AS 'MON', 
                COUNT(call_id) AS 'totConference', 
                CAST(IFNULL(SUM(calllegscompleted),0) AS UNSIGNED INTEGER) AS 'totCallLegs'
            FROM t
            LEFT JOIN 
                api_cdr_call acc
            ON acc.record_type = 'callEnd'
            AND DATE_FORMAT(acc.add_date,'%Y-%m') = t.ym
            group by t.ym
        '''
        statistics_list = TMUtility.get_query_to_list(statistics_query)

        context['result'] = "success"
        context['static_list'] = statistics_list

    except BaseException as e:

        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error(message)

        context['result'] = "server_err"
        context['tm_error'] = str(type(e).__name__)
        context['tm_error_detail'] = message
        context['static_list'] = list()

    finally:
        return JsonResponse(context)


def get_list(requset):
    context = dict()

    use_call = 0 
    call_flag = False
    total_resv = 0 # 전체 예약
    cur_resv = 0 # 금일 예약

    error_list = list() 
    activeCall_list = list() # 진행중 회의 목록
    cur_resv_list = list() # 현재 예약 회의 목록
    endCall_list = list() # 종료된 회의 목록

    # ------------------------ Reserve Conference ------------------------ #
    try:
        rct_query = '''
            SELECT
                IFNULL(SUM(CASE WHEN startdt > CURDATE() AND startdt < ADDDATE(CURDATE(),1) THEN 1 ELSE 0 END),0) AS curresv,
                IFNULL(SUM(1),0) AS totalresv
            FROM
                cms_reserve
            WHERE
                startdt > CURDATE()
                AND del_yn = 'N'
        '''
        rc_dict = TMUtility.get_query_to_dict(rct_query)
        total_resv = rc_dict['totalresv'] #Total Resvervation Count
        cur_resv = rc_dict['curresv']

    except BaseException as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error("@@@ get_list > Reserve Conference @@@ ")
        logger.error(message)
        total_resv = 0
        cur_resv = 0

    # ------------------------ Current Reservation ------------------------ #
    try:
        cur_resv_list_q = '''
            SELECT
                id,
                title,
                DATE_FORMAT(startdt,'%Y-%m-%d %H:%i') AS `startdt`
            FROM 
                cms_reserve
            WHERE startdt > curdate() 
                AND del_yn='N'
            UNION ALL
            SELECT '' AS 'id', '' AS 'title' , '' AS 'startdt'
            UNION ALL
            SELECT '' AS 'id', '' AS 'title' , '' AS 'startdt'
            UNION ALL
            SELECT '' AS 'id', '' AS 'title' , '' AS 'startdt'
            UNION ALL
            SELECT '' AS 'id', '' AS 'title' , '' AS 'startdt'
            UNION ALL
            SELECT '' AS 'id', '' AS 'title' , '' AS 'startdt'
            ORDER BY FIELD (startdt,NOT NULL,''), startdt asc
            LIMIT 5
        '''
        cur_resv_list = TMUtility.get_query_to_list(cur_resv_list_q)

    except BaseException as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error("@@@ get_list > Current Reservation @@@ ")
        logger.error(message)
        cur_resv_list = list()

    #------------------------ Acitve Call ---------------------------------------
    api_list = coreJson()['api']
    ca = CiscoApi()

    try:
        for group_list in api_list:
            temp_dict = dict()

            ca.setGroupSeqData(group_list)
            temp_dict['group_seq'] = group_list['group_seq']

            for group_data in group_list['api_list']:

                ca.setServerSeqData(group_data['seq'])
                call_list = ca.comCallAPI('calls','GET')

                if call_list['status'] == 200:
                    if not call_flag:
                        use_call = call_list['total']
                        call_flag = True

                    if call_list['total'] != 0:
                        calls_id = list()
                        for call_data in call_list['body']['calls']['call']:
                            calls_id.append(call_data['@id'])
                        loop = asyncio.new_event_loop()
                        temp_list = loop.run_until_complete(activecall_sub_1(loop, ca, group_data['seq'], group_list['group_seq'],group_list['group_name']))
                        loop.close()

                        for temp in temp_list:
                            activeCall_list.append(temp)
                else:
                    error_dict= dict()
                    error_dict['group_seq'] = group_list['group_seq']
                    error_dict['server_seq'] = group_data['seq']
                    error_dict['error'] = call_list['error']
                    error_list.append(error_dict)

        temp_del_num = list()
        for i in reversed(range(len(activeCall_list))):
            for j in reversed(range(len(activeCall_list))):
                if i==j:
                    pass
                elif j > i:
                    pass
                else:
                    if activeCall_list[i]['callCorrelator'] == activeCall_list[j]['callCorrelator']:
                        temp_del_num.append(i)

        temp_del_num = list(set(temp_del_num))
        temp_del_num.sort()

        for i in reversed(range(len(temp_del_num))):
            del activeCall_list[temp_del_num[i]]

        if len(activeCall_list) < 6:
            for i in range(0,5):
                length = len(activeCall_list)
                if length == 5:
                    break
                else:
                    activeCall_dict = dict()
                    activeCall_dict['durationSeconds'] = ''
                    activeCall_dict['@id'] = ''
                    activeCall_dict['name'] = ''
                    activeCall_dict['coSpace_id'] = ''
                    activeCall_list.append(activeCall_dict)
        else:
            activeCall_list = activeCall_list[0:5]

    except BaseException as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error("@@@ get_list > Acitve Call @@@ ")
        logger.error(message)
        activeCall_list = list()

    #------------------------------ Cospace list ---------------------------------------
    try:
        temp_list = list()
        temp_total = 0
        for group_list in api_list:
            temp_dict = dict()
            ca.setGroupSeqData(group_list)
            temp_dict['group_seq'] = group_list['group_seq']
            for group_data in group_list['api_list']:
                ca.setServerSeqData(group_data['seq'])
                cospace_list = ca.comCallAPI('coSpaces','GET')
                if cospace_list['status'] == 200:
                    if cospace_list['total'] > temp_total:
                        temp_total = cospace_list['total']
                        break
        total_conf = temp_total

    except BaseException as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error("@@@ get_list > Cospace list @@@ ")
        logger.error(message)
        total_conf = 0

    #------------------------------ Recently Terminated Conference ------------------------------
    try:
        endcall_query = '''
            SELECT 
                acc_s.call_id AS 'callguid',
                acc_s.name AS 'callname',
                acc_s.cospace AS 'cospaceguid',
                acc_e.calllegscompleted AS 'callLegsCompleted',
                acc_e.calllegsmaxactive AS 'callLegsMaxActive',
                acc_e.durationseconds AS 'callDurationSeconds',
                acc_s.add_date AS 'callStartTime', 
                acc_e.add_date AS 'callEndTime'
            FROM 
                api_cdr_call acc_s
            INNER JOIN api_cdr_call acc_e
                ON acc_s.call_id = acc_e.call_id
                AND acc_e.record_type = 'callEnd'
            WHERE 
                acc_s.cospace != '' 
                AND acc_s.add_date IS NOT NULL 
                AND acc_s.add_date != '' 
                AND acc_e.add_date IS NOT NULL 
                AND acc_e.add_date != ''
            UNION ALL 
            SELECT '' AS 'callguid', '' AS 'callname', '' AS 'cospaceguid', '' AS 'callLegsCompleted', '' AS 'callLegsMaxActive', '' AS 'callDurationSeconds', '' AS 'callStartTime', '' AS 'callEndTime'
            UNION ALL 
            SELECT '' AS 'callguid', '' AS 'callname', '' AS 'cospaceguid', '' AS 'callLegsCompleted', '' AS 'callLegsMaxActive', '' AS 'callDurationSeconds', '' AS 'callStartTime', '' AS 'callEndTime'
            UNION ALL 
            SELECT '' AS 'callguid', '' AS 'callname', '' AS 'cospaceguid', '' AS 'callLegsCompleted', '' AS 'callLegsMaxActive', '' AS 'callDurationSeconds', '' AS 'callStartTime', '' AS 'callEndTime'
            UNION ALL 
            SELECT '' AS 'callguid', '' AS 'callname', '' AS 'cospaceguid', '' AS 'callLegsCompleted', '' AS 'callLegsMaxActive', '' AS 'callDurationSeconds', '' AS 'callStartTime', '' AS 'callEndTime'
            UNION ALL 
            SELECT '' AS 'callguid', '' AS 'callname', '' AS 'cospaceguid', '' AS 'callLegsCompleted', '' AS 'callLegsMaxActive', '' AS 'callDurationSeconds', '' AS 'callStartTime', '' AS 'callEndTime'
            ORDER BY callEndTime DESC
            LIMIT 5
        '''
        endCall_list = TMUtility.get_query_to_list(endcall_query)

    except BaseException as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error("@@@ get_list > Recently Terminated Conference @@@ ")
        logger.error(message)
        endCall_list = list()

    context['total_resv'] = total_resv
    context['cur_resv'] = cur_resv
    context['total'] = total_conf
    context['use_call'] = use_call
    context['resv_list'] = cur_resv_list
    context['call_list'] = activeCall_list
    context['endcall_list'] = endCall_list
    context['chart_data'] = get_chart_data()

    return JsonResponse(context)

# MeetingInProgress 데이터 로드 비동기 Step1
async def activecall_sub_1(loop, ca, server_seq, group_seq, group_name):
    ca.setServerSeqData(server_seq)
    calls_list = ca.comCallAPI('calls','GET')
    if int(calls_list['total']) != 0:
        total = calls_list['total']
        futures = [asyncio.ensure_future(activecall_sub_1_fetch(loop, ca, server_seq, call_data, group_seq, group_name)) for call_data in calls_list['body']['calls']['call']]
        result = await asyncio.gather(*futures)
    else:
        result=dict()
    return result


# MeetingInProgress 데이터 로드 Step2
async def activecall_sub_1_fetch(loop, ca, server_seq, call_data, group_seq, group_name):
    ret_data = await loop.run_in_executor(None, activecall_sub_1_call_api, ca, server_seq, call_data, group_seq, group_name)
    return ret_data


# MeetingInProgress 데이터 로드 Step3
def activecall_sub_1_call_api(ca, server_seq, call_data, group_seq, group_name):
    re_data = dict()

    call_id = call_data['@id']
    re_data['group_seq'] = group_seq
    re_data['server_seq'] = server_seq

    data_call = ca.comCallAPI('calls/' + call_id, 'GET')

    try:
        if data_call['status'] == 200:
            if 'name' in data_call['body']['call']:
                re_data['name'] = data_call['body']['call']['name']
            else:
                re_data['name'] = ''
            re_data['call_guid'] = data_call['body']['call']['@id']
            if 'coSpace' in data_call['body']['call']:
                re_data['cospace_guid'] = data_call['body']['call']['coSpace']
            else:
                re_data['cospace_guid'] = ''
                
            re_data['callCorrelator'] = data_call['body']['call']['callCorrelator']
            re_data['durationSeconds'] = data_call['body']['call']['durationSeconds']

    except BaseException as e:

        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error("@@@ activecall_sub_1_call_api @@@ ")
        logger.error(message)

    finally:
        return re_data


def get_chart_data():
    context = dict()

    api_list = coreJson()['api']
    ca = CiscoApi()

    system_list = list()
    call_list = list()
    error_status_list = list()
    error_call_list = list()

    try:

        for group_list in api_list:
            ca.setGroupSeqData(group_list)
            for seq in group_list['api_list']:
                ca.setServerSeqData(seq['seq'])

                default_dict = dict()
                default_dict['server_seq'] = seq['seq']
                default_dict['group_seq'] = group_list['group_seq']
                default_dict['server_name'] = seq['serverName']

                resDataJson = ca.comCallAPI('system/status', 'GET')
                resDataJson2 = ca.comCallAPI('calls', 'GET')

                system_dict = dict(default_dict)
                call_dict = dict(default_dict)
                error_status_dict = dict(default_dict)
                error_call_dict = dict(default_dict)

                if 200 == resDataJson['status']:
                    system_dict['status'] = resDataJson['body']['status']
                else:
                    error_status_dict['status'] = resDataJson['status']
                    error_status_dict['error'] = resDataJson['error']
                    error_status_list.append(error_status_dict)

                if 200 == resDataJson['status']:
                    call_dict['call_total'] = resDataJson2['body']['calls']['@total']
                else:
                    error_call_dict['status'] = resDataJson['status']
                    error_call_dict['error'] = resDataJson['error']
                    error_call_list.append(error_call_dict)

                system_list.append(system_dict)
                call_list.append(call_dict)
        
    except BaseException as e:

        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        logger.error(message)

    finally:

        context['system_list'] = system_list
        context['call_list'] = call_list
        context['error_status_list'] = error_status_list
        context['error_call_list'] = error_call_list

        return context
