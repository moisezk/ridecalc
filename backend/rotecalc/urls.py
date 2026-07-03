from django.urls import path
from . import views



urlpatterns = [
    path('corridas/', views.corridas_app, name="corridas_app"),
    path('cadastro/', views.cadastro_app, name="cadastro_app"),
    path('login/', views.login_app, name="login_app"),
    path('historico/', views.historico_app, name="historico_app"),
    path('logout/', views.logout_app, name='logout_app'),
]