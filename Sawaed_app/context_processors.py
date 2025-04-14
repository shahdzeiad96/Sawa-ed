from .models import Notification

def notifications_processor(request):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:10]
        unread_notifications_count = notifications.filter(is_read=False).count()
        return {
            'notifications': notifications,
            'unread_notifications_count': unread_notifications_count,
        }
    return {}