from django.http import HttpResponse

def epic_view(request):
    return HttpResponse('EPIC')

def index_view(request):
    return HttpResponse('Department!')