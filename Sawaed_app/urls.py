from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.guest_home,name='guesthome'),
    path('userhome/', views.user_home, name='userhome'),
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
    path('send-message/<int:recipient_id>/', views.send_message, name='send-message'),
    path('mark-as-read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('add-to-cart/<int:service_id>/', views.add_to_cart, name='add-to-cart'),
    path('search/', views.search_services, name='service_search'),
    path('add-to-cart/<int:service_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:order_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-from-cart/<int:order_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('services/type/<str:service_type>/', views.services_by_type, name='services_by_type'),
    path('delete-service/', views.delete_service_ajax, name='delete_service_ajax'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('change-password/', views.password_change, name='password_change'),
    # path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('complete-order/<int:order_id>/', views.complete_order, name='complete_order'),
    path('orders/<int:order_id>/reject/', views.reject_order, name='reject_order'),
    path('orders/<int:order_id>/accept/', views.accept_order, name='accept_order'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),  
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),














]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)