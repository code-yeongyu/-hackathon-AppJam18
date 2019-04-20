from django.conf.urls import url
from articles import views

urlpatterns = [
    url(r'^images/thumbnail/(?P<pk>[0-9]+)/$',
        views.image_thumbnail),  # 이미지 썸네일을 얻는 라우트
    url(r'^images/(?P<pk>[0-9]+)/$', views.image),  # 이미지를 얻는 라우트
    url(r'^images/$', views.create_image),  # 이미지를 업로드하는 라우트
    url(r'^(?P<pk>[0-9]+)/$',
        views.ArticleDetail.as_view()),  # 해당되는 게시글을 얻는 라우트
    url(r'^$', views.ArticleList.as_view()),  # 게시글을 업로드하거나, 리스트를 얻을 수 있는 라우트
]
