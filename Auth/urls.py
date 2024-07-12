from django.urls import path 
from .views import Login, Logout, Register

urlpatterns = [
    path("login/", Login, name= 'login'),
    path('logout/', Logout, name= 'logout'),
    path('register/', Register, name= 'register')
]