from django.conf.urls import url, include
from . import views
app_name = 'app2'
urlpatterns = [
    url(r'^view1/(?P<param1>.+)/(?P<param2>.+)$', views.view1, name='app2_view1'),
    url(r'^view2/(.+)/(.+)$', views.view2, name='app2_view2'),
    url(r'^view3/(.+)/(.+)/(?P<param1>.+)/(?P<param2>.+)$', views.view3, name='app2_view3'),
    url(r'^app3/(?P<param1>.+)/(?P<param2>.+)/', include('js_reverse.tests.app3.urls', namespace='app3')),
]