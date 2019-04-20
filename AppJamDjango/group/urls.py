from django.conf.urls import url
from group import views

urlpatterns = [
    url(r'^join/(?P<pk>[0-9]+)/$', views.join_group),
    url(r'^', views.Group.as_view())
]
