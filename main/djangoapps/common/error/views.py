#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

def bad_request_page(request, *args, **argv):
    data = {}
    if request.is_ajax():
        return HttpResponse(status=400)
    return render(request,'common/error/400.html', data)

def page_not_found_page(request, *args, **argv):
    data = {}
    if request.is_ajax():
        return HttpResponse(status=404)
    return render(request,'common/error/404.html', data)

def server_error_page(request, *args, **argv):
    data = {}
    if 'user_id' not in request.session:
        data['error'] = 'notuserid'

    if 'user_role' not in request.session:
        data['error'] = 'notuserrole'

    if request.is_ajax():
        return HttpResponse(status=500)
    return render(request,'common/error/500.html', data)
