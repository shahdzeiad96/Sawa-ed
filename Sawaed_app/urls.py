from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart_view, name='cart'),
    path('userhome/', views.user_home, name='userhome'),
    path('add_service/', views.add_service, name='add_service'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('logout/', views.logout, name='logout'),
    path('service/<int:service_id>/<int:user_id>/', views.service_detail, name='service_detail'),
    path('send-message/<int:recipient_id>/<int:service_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('rate-service/<int:service_id>/', views.rate_service, name='rate_service'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)