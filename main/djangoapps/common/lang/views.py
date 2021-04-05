#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connections
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _

from backend.models import CmsManager

def transLang(request):

    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]

    userLanguage = request.POST.get('lang')
    userObject = CmsManager.objects.get(user_id=request.session['user_id'])
    userObject.language = userLanguage
    userObject.save()
    translation.activate(userLanguage)
    request.session[translation.LANGUAGE_SESSION_KEY] = userLanguage
    return JsonResponse({'return':'success'})
