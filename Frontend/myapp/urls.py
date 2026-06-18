from django.urls import path
from . import views



urlpatterns = [
    path("", views.app_view),
    path("app/",views.app_add)
]

