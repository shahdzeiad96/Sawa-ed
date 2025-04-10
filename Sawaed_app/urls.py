from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.user_home, name='userhome'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('userhome/', views.user_home, name='userhome'),
    path('add_service/', views.add_service, name='add_service'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('logout/', views.logout, name='logout'),
    path('service/<int:service_id>/<int:user_id>/', views.service_detail, name='service_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('rate-service/<int:service_id>/', views.rate_service, name='rate_service'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path("chat/", views.chatbot_ui, name="chat-ui"),
    path('chat/<int:user_id>/', views.chat_detail, name='chat_detail'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)