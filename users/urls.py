from .api import UserAPI, LoginAPI, RegisterAPI
from django.urls import path

from knox import views as knox_views

urlpatterns = [
    path('login/', LoginAPI.as_view(), name="login-api"),
    path('register/', RegisterAPI.as_view(), name="register-api"),
    path('user/', UserAPI.as_view(), name="user-api"),
    path('logout/', knox_views.LogoutView.as_view(), name='logout-api'),
]

