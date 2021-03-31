from django.urls import path
from . import views
urlpatterns = [
    path('main/', views.move_main, name = 'move_main' ),
    path('notice/', views.notice_list, name = 'notice_list' ),
    path('notice/detail',views.notice_search, name = 'notice_search' ),
    path('user/regist/', views.user_regist, name = 'user_regist' ),

]