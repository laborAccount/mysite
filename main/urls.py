from django.urls import path
from . import views
urlpatterns = [
    path('main/', views.move_main, name = 'move_main' ),
    path('notice/', views.notice_list, name = 'notice_list' ),
    path('notice/detail',views.notice_search, name = 'notice_search' ),
    path('notice/write' ,views.notice_write , name= 'notice_write'),
    path('notice/update' ,views.notice_update , name= 'notice_update'),
    path('notice/delete' ,views.notice_delete , name= 'notice_delete'),
    path('notice/save' ,views.notice_save , name= 'notice_save'),
    path('user/regist', views.user_regist, name = 'user_regist' ),
    path('user/regist/insert', views.user_insert, name = 'user_insert' ),
    
]