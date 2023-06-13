from os import name
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('user_get_post', views.UserGetPost.as_view(), name='user_get_post'),
    path('user_pk/<int:pk>', views.UserPk.as_view(), name='user_pk'),
    path('user_change_password', views.ChangePasswordView.as_view(), name='user_change_password'),
]