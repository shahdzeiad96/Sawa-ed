from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.index),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('userhome/',views.user_home,name='userhome'),
    path('add_service/', views.add_service, name='add_service'),
    path('profile/edit',views.edit_profile,name='edit-profile')
]

