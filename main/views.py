from django.shortcuts import render
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