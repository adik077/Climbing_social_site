from django.urls import path
from .views import login_user,logout_user,register,main_settings, change_password

urlpatterns = [
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path('register/',register,name='register'),
    path('main_settings/',main_settings,name='main_settings'),
    path('password/',change_password,name='change_password'),
]
