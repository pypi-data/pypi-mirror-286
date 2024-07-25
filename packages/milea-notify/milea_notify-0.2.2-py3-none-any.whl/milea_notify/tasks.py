from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_async(title, content, email):

    send_mail(
        title,
        content,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
