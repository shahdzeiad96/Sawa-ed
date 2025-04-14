from .models import Notifications

def notifications_processor(request):

    if request.user.is_authenticated:
        all_notifications = Notifications.objects.filter(recipient=request.user).order_by('-created_at')
        notifications = all_notifications[:10] 
        unread_notifications_count =all_notifications.filter(is_read=False).count()
        return {
            'notifications': notifications,
            'unread_notifications_count': unread_notifications_count,
        }
    return {}