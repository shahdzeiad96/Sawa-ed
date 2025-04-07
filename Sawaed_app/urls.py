from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.user_home,name='userhome'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('userhome/',views.user_home,name='userhome'),
    path('add_service/', views.add_service, name='add_service'),
<<<<<<< HEAD
    path('chatbot/', views.chatbot_response, name='chatbot')  #this path is temporary for chatbot later it will be added to the index page 
]
=======
    path('profile/edit',views.edit_profile,name='edit-profile'),
    path('logout/',views.logout,name='logout'),
    path('add_service/addservice', views.add_service, name='add_service'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 05f4f4ee7aa762280b9e34e86ae1f2ecdc54fb42

