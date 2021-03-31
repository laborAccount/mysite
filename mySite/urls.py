"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
#from main import views as mainViews
#from notice import views as noticeViews
#from user import views as userViews


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('notice/', noticeViews.notice_list, name = 'notice_list' ),
    #path('notice/detail', noticeViews.notice_search, name = 'notice_search' ),
    #path('user/regist/', userViews.user_regist, name = 'user_regist' ),
    #path('', mainViews.move_main, name = 'move_main' ),
    path('',include('main.urls'))
]
