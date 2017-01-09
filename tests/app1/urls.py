from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^view3$', views.view3, name='app1_view3'),
]