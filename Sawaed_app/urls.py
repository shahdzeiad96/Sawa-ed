from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.index),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('userhome/',views.user_home,name='userhome'),
    path('add_service/', views.add_service, name='add_service'),
    path('profile/edit',views.edit_profile,name='edit-profile'),
    path('logout/',views.logout,name='logout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

