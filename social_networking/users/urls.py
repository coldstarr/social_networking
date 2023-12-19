from django.contrib import admin
from django.urls import path, include
from . import  views

urlpatterns = [
    path('',views.Home.as_view()),
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('search/', views.UserSearchAPIView.as_view())
]
