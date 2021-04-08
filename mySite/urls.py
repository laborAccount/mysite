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
#from django.urls import path , include, url
from django.urls import path
from django.conf.urls import include, url
from main.djangoapps.meeting.room import views as meetingroom_view
from main.djangoapps.main import views as main_view
from main.djangoapps.common.base import views as BaseView
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^main$',main_view.main,name='main'),
    url(r'^main/read', main_view.main_read, name='main_read'),
    url(r'^main/get_list', main_view.get_list, name='get_list'),

    url(r'^login$', BaseView.login_ajax, name='login_ajax'),
    url(r'^$', BaseView.login, name='login'),


    url(r'^meetingroom$', meetingroom_view.meetingroom, name='meetingroom'),
    url(r'^meetingroom/list$', meetingroom_view.meetingroom_list, name='meetingroom_list'),
    url(r'^meetingroom/delete$', meetingroom_view.meetingroom_delete, name='meetingroom_delete')

]
