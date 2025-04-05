from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.index),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart_view, name='cart'),
]

