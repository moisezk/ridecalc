from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def app_view(request):
    return HttpResponse('welcome')

def app_add(request):
    return HttpResponse('evil')