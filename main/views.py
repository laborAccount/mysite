from django.shortcuts import render
from main.models import *
from datetime import datetime
from django.db import connection
# Create your views here.
# main page 이동
def move_main(request):
    print("--------------------------------------------------")
    print("move_main 함수")
    return render( request , 'main/main.html' )

def notice_list(request):
    print("--------------------------------------------------")
    print("notice_list 함수")

    noti_list = Test_Notice.objects.all()
    context = {'noti_list' : noti_list}
    print("context -> " , context)

    return render( request , 'notice/notice_list.html', context )

def notice_search(request):
    print("--------------------------------------------------")
    print("notice_search 함수")
    


    id = int(request.GET.get('id'))

    #print("id----->",id)
    if id is None or id =="" :
        print("id 값이 없습니다.")
    else :
        print("id 값이 존재")
    
    noti = Test_Notice.objects.get(pk=id)
    print("noti ->" ,noti)
    context = {'request_form':'search', 'noti': noti}
    print("context----------->",context)
    return render( request , 'notice/notice_detail.html' , context)

def notice_write(request):

    #list 에 선언된 form {저장 값 : user_id} 를 받아오기
    #user_id = request.POST.get('user_id')

    #print("--regist -> list -> notice 까지 토스가 잘 이루어졌는지 확인--")
    #print('user_id -> {0}'.format(user_id))

    #이제 다른 기능들은 다 세션에서 가져올예정
    #session_user_id = request.session['user_id']
    #print("session_user_id -> ", session_user_id)
    #if session_user_id is None or session_user_id =="" :
    #    return render( request, 'notice/notice_list.html')
    #
    now = datetime.now()
    print("now -->" ,now)
    noti = Test_Notice()
    noti.regist_dt = now
    print("noti.regist_dt -->" , noti.regist_dt)
    context = {'request_form':'write', 'noti' : noti}
    return render( request, 'notice/notice_detail.html',context)

def notice_save(request):
    #id = Test_Notice.objects.get(pk=1)
    #regist_id = request.POST.get("regist_id")
    notice_subject = request.POST.get("notice_subject")
    notice_memo = request.POST.get("notice_memo")
    regist_dt = request.POST.get("regist_dt")

    #print('@@ regitst_id =>', regist_id)
    print('@@ notice_subject =>', notice_subject)
    print('@@ notice_memo =>', notice_memo)
    print('@@ regist_dt =>', regist_dt)

    #noti = Test_Notice(notice_subject , notice_memo, regist_dt )\
    noti = Test_Notice()
    noti.notice_subject = notice_subject
    noti.notice_memo =notice_memo
    noti.regist_dt = regist_dt
    print('@@ noti =>', noti)
    noti.save()

    noti_list = Test_Notice.objects.all()
    context = {'noti_list' : noti_list}
    print("context -> " , context)

    return render(request ,'notice/notice_list.html',context)


def notice_update(request):
    id = request.POST.get("id")
    notice_subject = request.POST.get("notice_subject")
    notice_memo = request.POST.get("notice_memo")
    regist_dt = request.POST.get("regist_dt")

    noti = Test_Notice.objects.get(pk=id)
    noti.notice_subject = notice_subject
    noti.notice_memo = notice_memo
    noti.regist_dt = regist_dt

    noti.save()

    noti_list = Test_Notice.objects.all()
    context = {'noti_list' : noti_list}
    print("context -> " , context)
    return render(request ,'notice/notice_list.html',context)

def notice_delete(request):

    ids = request.POST.getlist("del_ids");
    print("ids -> ", ids)

    #noti_list.filter(id=ids).delete()
    #for notice in noti_list :
    #    print("notice.id -->", notice.id)
    #    print("ids(0)-->",ids[0] )
    #    if notice.id in ids :
    #       print("delete!! -->" , notice.id)
    #       notice.objects.delete()

    cursor = connection.cursor()
    cursor.execute(
        'DELETE FROM Main_Test_Notice WHERE id IN (%s)' % ', '.join(ids)
    )
    noti_list = Test_Notice.objects.all()
    context = {'noti_list' : noti_list}
    print("context -> " , context)
    return render(request, 'notice/notice_list.html', context)


def user_regist(request):
    print("--------------------------------------------------")
    print("user_regist 함수")
    return render( request , 'user/user_regist.html' )

def user_insert(request):
    print("--------------------------------------------------")
    print("user_insert 함수")

    user_name = request.POST.get('user_name')
    user_id = request.POST.get('user_id')
    user_password = request.POST.get('user_password')
    user_address = request.POST.get('user_address')
    user_birth = request.POST.get('user_birth')
    user_call = request.POST.get('user_call')
    user_email = request.POST.get('user_email')

    print('user_name : {0} '.format(user_name))
    print('user_id : {0} '.format(user_id))
    print('user_password : {0} '.format(user_password))
    print('user_address : {0} '.format(user_address))
    print('user_birth : {0} '.format(user_birth))
    print('user_call : {0} '.format(user_call))
    print('user_email : {0} '.format(user_email))

    tui = None
    if user_name is not None and user_id is not None and user_password is not None :
        tui = Test_User_Info(user_name, user_id, user_password, user_address, user_birth, user_call , user_email)
        print('TUI INFO => {0}'.format(tui))
        
    try:
        if tui is not None :
            tui.save()
    except :
        tui = None
    # 세션에 저장하였지만 form에 담아 dom을 이용하여 전달하려고 일부러 보냄
    context = { 'user_id' : user_id }
    save_session( request , user_id)
    
    return render(request , 'notice/notice_list.html', context )

def save_session(request, user_id):
    request.session['user_id'] = user_id
