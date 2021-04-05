# -*- coding: utf-8 -*-
from django.http.request import QueryDict

def requestToDict(request):

    rtn_dict = dict()

    if request.method == 'GET':
        rtn_dict = request.GET.dict()
        
    elif request.method == 'POST':
        if type(request.data) == type(QueryDict()):
            rtn_dict = request.data.dict()
        else:
            rtn_dict = request.data

    elif request.method == 'PUT':
        if type(request.data) == type(QueryDict()):
            rtn_dict = request.data.dict()
        else:
            rtn_dict = request.data
            
    elif request.method == 'DELETE':
        if type(request.data) == type(QueryDict()):
            rtn_dict = request.data.dict()
        else:
            rtn_dict = request.data
            
    return rtn_dict