from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^api/articles/', include('articles.urls')),
    url(r'^api/account/', include('custom_account.urls')),
    url(r'^api/group/', include('group.urls'))
]


urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns = urlpatterns + [
    url(r'^api/token-auth/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
]
