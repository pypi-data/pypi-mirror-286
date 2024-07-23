from django import template

from milea_notify.models import Notification

register = template.Library()

@register.inclusion_tag('milea_notify/header_notifications.html', takes_context=True)
def header_notifications(context):

    user = context['request'].user
    if user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=user, is_read=False).order_by('-is_important', '-created_at')
        has_important = unread_notifications.filter(is_important=True).exists()
        return {'has_important': has_important, 'unread_notifications': unread_notifications}
    else:
        return {'has_important': False, 'unread_notifications': []}
