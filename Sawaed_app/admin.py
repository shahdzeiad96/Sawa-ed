from django.contrib import admin
from .models import (
    CustomUser,
    ServiceListing,
    HandymanProfile,
    Application,
    Review,
    Appointment,
    Message,
    CartItem,
    ServiceOrder,
    Notifications
)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('user_type',)

@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'handyman', 'service_type', 'price', 'created_at')
    search_fields = ('name', 'handyman__username')
    list_filter = ('service_type',)

@admin.register(HandymanProfile)
class HandymanProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'availability', 'rating')
    search_fields = ('user__username',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'worker', 'status', 'created_at')
    search_fields = ('worker__username', 'job__name')
    list_filter = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'rating', 'created_at')
    search_fields = ('client__username', 'service__name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date_time', 'status')
    list_filter = ('status',)
    search_fields = ('client__username', 'service__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('is_read',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'added_at')
    search_fields = ('user__username', 'service__name')

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'handyman', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('client__username', 'handyman__username', 'service__name')

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'verb', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('recipient__username', 'verb')
