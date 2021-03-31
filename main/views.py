from django.shortcuts import render
# Create your views here.
# main page 이동
def move_main(request):
    print("--------------------------------------------------")
    return render( request , 'main.html' )