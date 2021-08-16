from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(name="send_email_task")
def send_email_task(data):
    send_mail(
        subject=data['email_subject'], 
        message=data['email_body'], 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[data['to_email']],
        fail_silently=False
        )
    return "Done!"