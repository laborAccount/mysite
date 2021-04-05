#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.db import connections
from django.utils import translation
from backend.models import CmsManager

from backend.djangoapps.common.core.views import coreJson
from logging import handlers

# api 전체 서버 정보
from backend.djangoapps.common.core.views import coreJson

# api 공통
from backend.djangoapps.common.api.views import callApi , callApiBasic
from backend.djangoapps.common.com.views import CiscoApi
from backend.djangoapps.common.core.views import coreJson
from datetime import timedelta

import logging
import logging.config
import datetime
import calendar
import requests
import json
import asyncio
from backend.models import CmsCospace

def batch(request):

    ca = CiscoApi()

    with connections['default'].cursor() as cur:
        query = '''
          SELECT id, callid, title, passcode, group_seq, server_seq
          FROM cms_reserve
          WHERE call_yn = 'N'
            AND del_yn = 'N'
            AND startdt >= curdate()
            AND startdt <= now()
          ORDER BY startdt ASC
        '''
        cur.execute(query)
        rows = cur.fetchall()
    if len(rows) != 0:
        for row in rows:

            seq = row[0]
            call_id = row[1]
            call_name = row[2]

            payload = dict()
            payload['name'] = call_name
            payload['uri'] = call_id
            payload['callId'] = call_id
            payload['passcode'] = row[3]

            ca.setGroupSeq(row[4])
            ca.setServerSeqData(row[5])
            res = ca.comCallAPI('coSpaces', 'POST', jsonParam=payload)

            if 200 == res['status'] :
                header = res['headers']['Location']
                cospace_guid = header.split('/')[-1]


                CmsCospace.objects.create(cospace_id = cospace_guid,
                                          name = payload['name'],
                                          uri = payload['uri'],
                                          call_id = payload['callId'],
                                          passcode = payload['passcode'],
                                          group_seq = int(row[4]),
                                          server_seq = int(row[5]),
                                          regist_date=datetime.datetime.now(),
                                          regist_id='system')
                payload = {
                    'coSpace': cospace_guid,
                }

                res = ca.comCallAPI('calls', 'POST', jsonParam=payload)
                if 200 == res['status']:

                    header = res['headers']['Location']
                    call_guid = header.split('/')[-1]
                    with connections['default'].cursor() as cur:
                        query = '''
                            UPDATE cms_reserve
                            SET call_yn = 'Y',
                                cospace_guid = '{cospace_guid}',
                                call_guid = '{call_guid}'
                            WHERE id = '{seq}'
                        '''.format(seq=seq, cospace_guid = cospace_guid, call_guid = call_guid)
                        cur.execute(query)

                    participant_list = list()
                    with connections['default'].cursor() as cur:
                        query = '''
                          SELECT id,callnumber, name, namelabeloverride, qualitymain, qualitypresentation, bandwidth, dtmf,
                          txaudiomute, rxaudiomute, txvideomute, rxvideomute, presentationviewingallowed, presentationcontributionallowed
                          FROM cms_reserve_participant
                          WHERE resvseq = '{seq}' and del_yn = 'N'
                        '''.format(seq = seq)
                        cur.execute(query)
                        participant_list = list(cur.fetchall())
                     # participant 초대
                    loop = asyncio.new_event_loop()
                    loop_result = loop.run_until_complete(callleg_invite_sub(loop, ca, participant_list, call_guid))
                    loop.close()

    return JsonResponse({'a': 'b'})

async def callleg_invite_sub(loop, ca, participant_list, call_guid):
    futures = [asyncio.ensure_future(
        callleg_invite_sub_fetch(loop, ca, participant_data, call_guid))
        for participant_data in participant_list]
    result = await asyncio.gather(*futures)
    temp_dict = dict()
    temp_dict['data_list'] = result
    return temp_dict


async def callleg_invite_sub_fetch(loop, ca, participant_data, call_guid):
    ret_data = await loop.run_in_executor(None, callleg_invite_sub_fetch_fn, ca, participant_data, call_guid)
    return ret_data


def callleg_invite_sub_fetch_fn(ca, participant_data, call_guid):
    result = 'success'
    jsonParam = set_param(participant_data)
    t_callLegs = ca.comCallAPI('calls/{id}/callLegs'.format(id=call_guid), 'POST', jsonParam=jsonParam)
    if t_callLegs['status'] == 200:
        callleg_guid = t_callLegs['headers']['Location'].split('/')[-1]
        with connections['default'].cursor() as cur:
            query = '''
                UPDATE cms_reserve_participant
                SET
                    callleg_guid = '{callleg_guid}',
                    invite_yn = 'Y',
                    invite_date = now()
                WHERE id = '{id}'
            '''.format(callleg_guid=callleg_guid, id=participant_data[0])
            cur.execute(query)
    else:
        with connections['default'].cursor() as cur:
            query = '''
                UPDATE cms_reserve_participant
                SET
                    invite_yn = 'N',
                    invite_date = now()
                WHERE id = '{id}'
            '''.format(id=participant_data[0])
            cur.execute(query)
    return result


def set_param(participant_data):
    jsonParam = dict()
    jsonParam['remoteParty'] = participant_data[1]
    jsonParam['name'] = participant_data[2]
    if participant_data[2] != '':
        jsonParam['nameLabelOverride'] =  participant_data[3]
    jsonParam['qualityMain'] = participant_data[4]
    jsonParam['qualityPresentation'] = participant_data[5]
    jsonParam['bandwidth'] = participant_data[6]
    jsonParam['dtmfSequence'] = participant_data[7]
    jsonParam['txAudioMute'] = set_tf(participant_data[8])
    jsonParam['rxAudioMute'] = set_tf(participant_data[9])
    jsonParam['txVideoMute'] = set_tf(participant_data[10])
    jsonParam['rxVideoMute'] = set_tf(participant_data[11])
    jsonParam['presentationViewingAllowed'] = set_tf(participant_data[12])
    jsonParam['presentationContributionAllowed'] = set_tf(participant_data[13])
    return jsonParam

def set_tf(value):
    if value == 'Y':
        return 'true'
    else:
        return 'false'

def delete_batch(request):
    ca = CiscoApi()

    with connections['default'].cursor() as cur:
        query = '''
          SELECT id, cospace_guid, group_seq, server_seq
          FROM cms_reserve
          WHERE call_yn = 'Y'
            AND del_yn = 'N'
            AND enddt <= now()
          ORDER BY enddt ASC
        '''
        cur.execute(query)
        rows = cur.fetchall()
    if len(rows) != 0:
        for row in rows:
            resvseq = row[0]
            cospace_guid = row[1]
            ca.setGroupSeq(row[2])
            ca.setServerSeqData(row[3])
            res = ca.comCallAPI('coSpaces/{cospace_guid}'.format(cospace_guid = cospace_guid), 'DELETE')
            if res['status'] == 200:
                with connections['default'].cursor() as cur:
                    query = '''
                      UPDATE cms_reserve
                      SET
                        del_yn = 'Y',
                        modify_date = now()
                      WHERE id = '{resvseq}'
                    '''.format(resvseq = resvseq)
                    cur.execute(query)

                    query = '''
                      UPDATE cms_reserve_participant
                      SET
                        del_yn = 'Y',
                        modify_date = now()
                      WHERE resvseq = '{resvseq}'
                    '''.format(resvseq = resvseq)
                    cur.execute(query)
                result = CmsCospace.objects.filter(cospace_id = cospace_guid,delete_yn = 'N').update(modify_id = 'system',delete_yn = 'Y')
    return JsonResponse({'a': 'b'})
