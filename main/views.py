from django.shortcuts import render
from main.models import *
# Create your views here.
# main page 이동
def move_main(request):
    print("--------------------------------------------------")
    print("move_main 함수")
    return render( request , 'main/main.html' )

def notice_list(request):
    print("--------------------------------------------------")
    print("notice_list 함수")
    return render( request , 'notice/notice_list.html' )

def notice_search(request):
    print("--------------------------------------------------")
    print("notice_search 함수")
    return render( request , 'notice/notice_detail.html' )

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

    context = { 'user_id' : user_id }

    return render(request , 'notice/notice_list.html', context )