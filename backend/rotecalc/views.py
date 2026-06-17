from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def corridas_app(request):
    return render(request, 'corridas.html')