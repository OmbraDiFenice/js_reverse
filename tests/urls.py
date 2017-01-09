from django.conf.urls import url, include

from django.shortcuts import render

def test(request):
    return render(request, "js_reverse/test.html")

import js_reverse.tests.app1.views
urlpatterns = [
    url(r'^app1$', js_reverse.tests.app1.views.view1),
    url(r'^app1/view2/(?P<param1>.+)$', js_reverse.tests.app1.views.view2, name='app1_view2'),
    url(r'^app1/', include('js_reverse.tests.app1.urls', namespace='app1')),
    url(r'^app2/', include('js_reverse.tests.app2.urls')),
    url(r'^$', test, name='test'),
]