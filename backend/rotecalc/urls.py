from django.urls import path
from . import views



urlpatterns = [
    path('corridas/', views.corridas_app, name="corridas_app")
]