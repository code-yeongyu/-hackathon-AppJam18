from django.conf.urls import url
from custom_account import views

urlpatterns = [
    url(r'^signup/$', views.sign_up),  # 회원가입 요청을 넣는 라우트
    url(r'^change/username/$', views.change_username),  # 유저 이름을 변경하는 라우트
    url(r'^(?P<string>[\w\-]+)/$',
        views.ProfileDetail.as_view()),  # <유저 이름>의 프로필을 조회 하는 라우트
    url(r'^$', views.ProfileOverall.as_view()),  # 프로필 정보를 얻거나 , 변경하는 라우트
]
