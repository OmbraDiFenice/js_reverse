from django.http import HttpResponse

def view1(request):
    return HttpResponse("app2 - view1")
def view2(request):
    return HttpResponse("app2 - view2")
def view3(request):
    return HttpResponse("app2 - view3")