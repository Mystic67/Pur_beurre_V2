from django.conf.urls import url
from . import views

app_name = "accounts"

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='enregistrement')
]
