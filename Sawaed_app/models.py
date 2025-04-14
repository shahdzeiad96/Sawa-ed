from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import RegexValidator
class CustomUser(AbstractUser): 
    class UserType(models.TextChoices):
        CLIENT = 'client', _('عميل')
        HANDYMAN = 'handyman', _('عامل يدوي') #the name in arabic will be edited later
        # ADMIN = 'admin', _('مسؤول') 
        # not sure if we need it here just remove the comment and run the migrations if we need it later  in the project 
    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
        default=UserType.CLIENT
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', #a validation on the phone number because its customed 
        message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
    )
    image = models.ImageField(upload_to='profile_pics/',default='default_profile.jpeg' ,null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=500, blank=True, null=True)  
    experience = models.TextField(blank=True, null=True) 
    field_of_expertise=models.TextField(blank=True, null=True)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'  # we could change it to email later in the project 
    def __str__(self):
        return f"{self.username} ({self.user_type})" 
        
class ServiceListing(models.Model):

    SERVICE_TYPES = [
        ('السباكة', 'السباكة'),
        ('النجارة', 'النجارة'),
        ('الطبخ', 'الطبخ'),
        ('التصوير', 'التصوير'),
        ('الكهرباء', 'الكهرباء'),
        ('التكييف والتبريد', 'التكييف والتبريد'),
        ('التنظيف', 'التنظيف'),
        ('الميكانيكا', 'الميكانيكا'),
        ('الدهان', 'الدهان'),
        ('الحدادة', 'الحدادة'),
        ('التمديدات الصحية', 'التمديدات الصحية'),
        ('البرمجة وتطوير المواقع', 'البرمجة وتطوير المواقع'),
        ('التصميم الجرافيكي', 'التصميم الجرافيكي'),
        ('الترجمة', 'الترجمة'),
        ('الكتابة والتحرير', 'الكتابة والتحرير'),
        ('خدمات أخرى', 'خدمات أخرى'), 
    ]

    handyman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, null=True, blank=True,default='خدمات أخرى')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class HandymanProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='handyman_profile'
    )
    location = models.CharField(max_length=255)
    availability = models.BooleanField(null=True) 
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Handyman Profile"

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')

    job = models.ForeignKey(ServiceListing, on_delete=models.CASCADE)
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.worker.username} -> {self.job.name}"


class Review(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_reviews'
    )
    service = models.ForeignKey(ServiceListing, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.username} Review"

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        CONFIRMED = 'confirmed', _('Confirmed')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    service = models.ForeignKey(ServiceListing, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.username} - {self.service.name} - {self.status}"
    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    service = models.ForeignKey(
        ServiceListing, 
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
    
class ServiceOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('rejected', _('Rejected')),
    ]
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    service = models.ForeignKey(
        ServiceListing, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    handyman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_orders',
        null=True,
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.client.username} - {self.service.name} ({self.status})"
    
class Notifications(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="notifications"
        )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank = True,
        on_delete=models.SET_NULL,
        related_name="actor_notification"
        )
    verb = models.CharField(max_length=40, null=True)
    service_order = models.ForeignKey(
            ServiceOrder, 
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            related_name="notifications"
        )
    message = models.TextField(null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Notifications for {self.recipient.username}: {self.verb}"