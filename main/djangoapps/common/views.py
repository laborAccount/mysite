#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connections

import json


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
                JOIN cms_code_detail d ON a.up_menu_seq = d.detail_code
                JOIN cms_manager_menu c ON c.menu_seq = a.menu_seq
                JOIN cms_manager b  ON b.user_id = c.user_id
                INNER JOIN cms_menu_default e ON e.user_role = b.user_role AND e.menu_seq = c.menu_seq AND e.default_yn = 'Y'
                WHERE b.user_role = '{user_role}' AND b.user_id ='{user_id}' AND a.delete_yn='N' AND e.default_yn = 'Y'
                GROUP BY menu_seq
                ORDER BY sort_no
        '''.format(user_role=user_role,user_id=user_id)
        cur.execute(query)
        rows = cur.fetchall()

        context = []
        check = 'xxx'
        for row in rows:
            dict = {}
            if check != row[0]:
                dict['menu'] = row[0]
                dict['menu_class'] = row[5]
                dict['submenu'] = []

                if row[6] == row[1]:
                    dict['menu_url'] = row[4]
                    #context.append(dict)
                context.append(dict)
                check = row[0]
        for item in context:
            for row in rows:
                if item['menu'] == row[0]:
                    if row[6] != row[1]:
                        item['submenu'].append([row[4], row[2]])

    return JsonResponse({'return':context})
