import json
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

from backend.djangoapps.common.encrypt.views import AESCipher
#jwt
from django.core.exceptions import PermissionDenied
from http import HTTPStatus
import hmac
import hashlib
import json


class customSessionMiddleware:
    SETTINGS = None

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)   # view 호출된 후
        self.post_check_user_session(request,response)
        # self.post_check_license(request,response)
        return response

    # pre_세션 체크
    def pre_check_user_session(self, request):
        if request.get_full_path().find("static") == -1 and request.get_full_path().find("login") == -1:
            if request.is_ajax():
                if 'user_id' not in request.session or 'user_role' not in request.session:
                    return JsonResponse({"tmAuth":False})
            else:
                if 'user_id' not in request.session or 'user_role' not in request.session:
                    context = {}
                    return render(request, 'common/error/session.html', context)

    # post_세션 체크
    def post_check_user_session(self, request, response):
        if request.get_full_path().find("static") == -1 and request.get_full_path().find("login") == -1:
            if request.is_ajax():
                if type(JsonResponse({})) == type(response):
                    if 'user_id' not in request.session or 'user_role' not in request.session:
                        tempJson = json.loads(response.content.decode("utf-8"))
                        tempJson['tmAuth'] = False
                        response.content = json.dumps(tempJson).encode("utf-8")
                        response.status_code = 401
                        return response
                    else :
                        tempJson = json.loads(response.content.decode("utf-8"))
                        tempJson['tmAuth'] = True
                        response.content = json.dumps(tempJson).encode("utf-8")
                        return

            else :
                context = {}
                if 'user_id' not in request.session or 'user_role' not in request.session:
                    return render(request, 'common/error/session.html', context)

    # post_라이센스 체크
    def post_check_license(self,request,response):
        if not request.is_ajax():
            license_key = settings.LICENSE
            key = settings.AES_KEY
            ac = AESCipher(key)
            decode_key = ac.decrypt(license_key)
            decode_key.split('h4ppyy')
            check_data = decode_key.split('h4ppyy')[0]
            check_time = decode_key.split('h4ppyy')[1]
            now_date = datetime.strptime(str(datetime.now()).split(' ')[0],"%Y-%m-%d").date()
            license_date = datetime.strptime(check_time,"%Y-%m-%d").date()

            if now_date > license_date and settings.LICENSE_CHECK == 'Y':
                context = {}
                context['warning'] = 'license'
                return render(request, 'common/error/session.html', context)

    # post_서버 개수 체크
    def post_check_server_count(self,request,response):
        pass


#jwt middleware
class JsonWebTokenMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path_url = request.META['PATH_INFO']
        
        try:
            
            if path_url.find("/api/v1") != -1:
                if request.META['REQUEST_METHOD'] != 'GET':
                    if request.META['CONTENT_TYPE'] != 'application/json':
                        return JsonResponse(
                            {"error": "Content Type Error"}, status=HTTPStatus.BAD_REQUEST
                        )
                API_SECRET = settings.API_SECRET_KEY
                json_data = QueryDictToDict(request)
                message = json.dumps(json_data)

                signature = hmac.new(
                    bytes(str(API_SECRET), encoding='utf-8'),
                    msg = bytes(message, encoding='utf-8'),
                    digestmod=hashlib.sha256
                ).hexdigest()

                if 'HTTP_SECRETKEY' in request.META:
                    key = request.META['HTTP_SECRETKEY']
                    if key:
                        if not key == signature:
                            raise PermissionDenied()
                    else:
                        raise PermissionDenied()
                    
                else:
                    raise PermissionDenied()

                response = self.get_response(request)
                return response

            else:
                response = self.get_response(request)
                return response

        except (PermissionDenied):
            print(request.META)
            return JsonResponse(
                {"error": "Authorization Error"}, status=HTTPStatus.UNAUTHORIZED
            )

def QueryDictToDict(request):
    if request.method == 'GET':
        return request.GET.dict()
    elif request.method == 'POST':
        json_data = json.loads(request.body)
        return json_data
    elif request.method == 'PUT':
        json_data = json.loads(request.body)
        return json_data
    elif request.method == 'DELETE':
        json_data = json.loads(request.body)
        return json_data