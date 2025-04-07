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
    path('chatbot/', views.chatbot_response, name='chatbot')  #this path is temporary for chatbot later it will be added to the index page 
]

