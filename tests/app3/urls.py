from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^view1/(?P<param3>.+)/(?P<param4>.+)$', views.view1, name='app3_view1'),
    url(r'^view2/(.+)/(.+)$', views.view2, name='app3_view2'),
    url(r'^view3/(?P<param3>.+)/(?P<param4>.+)/(.+)/(.+)$', views.view3, name='app3_view3'),
]